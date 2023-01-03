"""
General utilities for the MPESA functions
"""

from __future__ import print_function
from .exceptions import MpesaConfigurationException, IllegalPhoneNumberException, MpesaConnectionError, MpesaError
from django_daraja.models import AccessToken
import requests
from django.utils import timezone
from decouple import config, UndefinedValueError
import os
from requests import Response
import time
from django.conf import settings
import os
from django.conf import settings
import base64
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15


class MpesaResponse(Response):
	request_id = ''
	response_code = ''
	response_description = ''
	customer_message = ''
	conversation_id = ''
	originator_conversation_id = ''
	error_code = ''
	error_message = ''
	merchant_request_id = ''
	checkout_request_id = ''


def mpesa_response(r):
	"""
	Create MpesaResponse object from requests.Response object
	
	Arguments:
		r (requests.Response) -- The response to convert
	"""

	r.__class__ = MpesaResponse
	json_response = r.json()
	r.request_id = json_response.get('requestId', '')
	r.response_code = json_response.get('ResponseCode', '')
	r.response_description = json_response.get('ResponseDescription', '')
	r.customer_message = json_response.get('CustomerMessage', '')
	r.conversation_id = json_response.get('ConversationID', '')
	r.originator_conversation_id = json_response.get('OriginatorConversationID', '')
	r.error_code = json_response.get('errorCode')
	r.error_message = json_response.get('errorMessage', '')
	r.merchant_request_id = json_response.get('MerchantRequestID', '')
	r.checkout_request_id = json_response.get('CheckoutRequestID', '')
	return r


def mpesa_config(key):
	"""
	Get Mpesa configuration variable with the matching key
	
	Arguments:
		key (str) -- The configuration key

	Returns:
		str: Mpesa configuration variable with the matching key

	Raises:
		MpesaConfigurationException: Key not found
	"""

	value = getattr(settings, key, None)
	if value is None:
		try:
			value = config(key)
		except UndefinedValueError:
			# Check key in settings file
			raise MpesaConfigurationException('Mpesa environment not configured properly - ' + key + ' not found')

	return value


def api_base_url():
	"""
	Gets the base URL for making API calls

	Returns:
		The base URL depending on development environment (sandbox or production)

	Raises:
		MpesaConfigurationException: Environment not sandbox or production
	"""

	mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')

	if mpesa_environment == 'development':
		return 'https://darajasimulator.azurewebsites.net/'
	elif mpesa_environment == 'sandbox':
		return 'https://sandbox.safaricom.co.ke/'
	elif mpesa_environment == 'production':
		return 'https://api.safaricom.co.ke/'
	else:
		raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

def generate_access_token_request(consumer_key = None, consumer_secret = None):
	"""
	Make a call to OAuth API to generate access token
	
	Arguments:
		consumer_key (str) -- (Optional) The Consumer Key to use
		consumer_secret (str) -- (Optional) The Consumer Secret to use

	Returns:
		requests.Response: Response object with the response details

	Raises:
		MpesaConnectionError: Connection error
	"""

	url = api_base_url() + 'oauth/v1/generate?grant_type=client_credentials'
	consumer_key = consumer_key if consumer_key is not None else mpesa_config('MPESA_CONSUMER_KEY') 
	consumer_secret = consumer_secret if consumer_secret is not None else mpesa_config('MPESA_CONSUMER_SECRET')

	try:
		r = requests.get(url, auth=(consumer_key, consumer_secret))
	except requests.exceptions.ConnectionError:
		raise MpesaConnectionError('Connection failed')
	except Exception as ex:
		return ex.message
	
	return r

def generate_access_token():
	"""
	Parse generated OAuth access token, then updates database access token value

	Returns:
		AccessToken: The AccessToken object from the database

	Raises:
		MpesaError: Error generating access token
	"""

	r = generate_access_token_request()
	if r.status_code != 200:
		# Retry to generate access token
		r = generate_access_token_request()
		if r.status_code != 200:
			raise MpesaError('Unable to generate access token')

	token = r.json()['access_token']

	AccessToken.objects.all().delete()
	access_token = AccessToken.objects.create(token=token)

	return access_token

def mpesa_access_token():
	"""
	Generate access token if the current one has expired or if token is non-existent
	Otherwise return existing access token

	Returns:
		str: A valid access token
	"""

	access_token = AccessToken.objects.first()
	if access_token == None:
		# No access token found
		access_token = generate_access_token()
	else:
		delta = timezone.now() - access_token.created_at
		minutes = (delta.total_seconds()//60)
		if minutes > 50:
			# Access token expired
			access_token = generate_access_token()	
	
	return access_token.token

def format_phone_number(phone_number):
	"""
	Format phone number into the format 2547XXXXXXXX
	
	Arguments:
		phone_number (str) -- The phone number to format
	"""

	if len(phone_number) < 9:
		raise IllegalPhoneNumberException('Phone number too short')
	else:
		return '254' + phone_number[-9:]

def encrypt_security_credential(credential):
	"""
	Generate an encrypted security credential from a plaintext value
	
	Arguments:
		credential (str) -- The plaintext credential display
	"""

	mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')

	if mpesa_environment in ('development', 'sandbox', 'production'):
		certificate_name = mpesa_environment + '.cer'
	else:
		raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

	certificate_path = os.path.join(settings.BASE_DIR, 'certs', certificate_name)
	return encrypt_rsa(certificate_path, credential)

def encrypt_rsa(certificate_path, input):
	message = input.encode('ascii')
	with open(certificate_path, "rb") as cert_file:
		cert = x509.load_pem_x509_certificate(cert_file.read())
		encrypted = cert.public_key().encrypt(message, PKCS1v15())
		output = base64.b64encode(encrypted).decode('ascii')

	return output
