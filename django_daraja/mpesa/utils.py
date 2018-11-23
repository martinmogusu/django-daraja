'''
General utilities for the MPESA functions
'''

from __future__ import print_function
from .exceptions import *
from django_daraja.models import AccessToken
import requests
import json
from django.utils import timezone
from decouple import config, UndefinedValueError
import os
from requests import Response
import time


class MpesaResponse(Response):
	response_description = ""
	error_code = None
	error_message = ''


def mpesa_response(r):
	'''
	Creates MpesaResponse object from requests.Response object
	
	Arguments:
		r {requests.Response} -- The response to convert
	'''

	r.__class__ = MpesaResponse
	json_response = r.json()
	r.response_description = json_response.get('ResponseDescription', '')
	r.error_code = json_response.get('errorCode')
	r.error_message = json_response.get('errorMessage', '')
	return r


def mpesa_config(key):
	'''
	Gets Mpesa configuration variable with the matching key, otherwise returns MpesaConfigurationException
	
	Arguments:
		key {str} -- The configuration key
	'''

	try:
		value = config(key)
	except UndefinedValueError:
		# Check key in settings file
		raise MpesaConfigurationException('Mpesa environment not configured properly - ' + key + ' not found')

	return value


def api_base_url():
	'''
	Gets the base URL depending on the development environment (sandbox or production)
	'''

	mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')

	if mpesa_environment == 'sandbox':
		return 'https://sandbox.safaricom.co.ke/'
	elif mpesa_environment == 'production':
		return 'https://api.safaricom.co.ke/'
	else:
		raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

def generate_access_token_request(consumer_key = None, consumer_secret = None):
	'''
	Makes call to OAuth API
	'''

	url = api_base_url() + 'oauth/v1/generate?grant_type=client_credentials'
	consumer_key = consumer_key if consumer_key is not None else mpesa_config('MPESA_CONSUMER_KEY') 
	consumer_secret = consumer_secret if consumer_secret is not None else mpesa_config('MPESA_CONSUMER_SECRET')

	try:
		r = requests.get(url, auth=(consumer_key, consumer_secret))
	except requests.exceptions.ConnectionError:
		raise MpesaConnectionError('Connection failed')
	except Exception:
		return ex.message
	
	return r

def generate_access_token():
	'''
	Parses OAuth response to generate access token, then updates database access token value
	'''

	r = generate_access_token_request()
	token = json.loads(r.text)['access_token']

	AccessToken.objects.all().delete()
	access_token = AccessToken.objects.create(token=token)

	return access_token

def mpesa_access_token():
	'''
	Generates access token if the current one has expired or if token is non-existent
	Otherwise returns existing access token
	'''

	# access_token = generate_access_token()

	access_token = AccessToken.objects.first()
	if access_token == None:
		# No access token found
		access_token = generate_access_token()
	else:
		delta = timezone.now() - access_token.created_at
		minutes = (delta.total_seconds()//60)%60
		print('minutes: ', minutes)
		if minutes > 50:
			# Access token expired
			access_token = generate_access_token()	
	
	return access_token.token

def format_phone_number(phone_number):
	'''
	Formats phone number into the format 2547XXXXXXXX
	'''

	if len(phone_number) < 9:
		raise IllegalPhoneNumberException('Phone number too short')
	else:
		return '254' + phone_number[-9:]

def sleep(seconds, message=''):
	'''
	Sleeps for the specified number of seconds
	
	Arguments:
		seconds {float} -- Number of seconds to sleep, can be a float
		message {str} -- (Optional) message to display
	'''

	print()
	print('===')
	print(message, end="")
	for i in range(seconds * 2):
		time.sleep(0.5)
		print('.', end="")
	print()
	print('===')
	print()