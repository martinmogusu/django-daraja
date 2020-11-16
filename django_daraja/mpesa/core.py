import requests
from requests.auth import HTTPDigestAuth
import base64
from datetime import datetime
import json
from .exceptions import MpesaInvalidParameterException, MpesaConnectionError
from .utils import encrypt_security_credential, mpesa_access_token, format_phone_number, api_base_url, mpesa_config, mpesa_response
from decouple import config

class MpesaClient:
	"""
	This is the core MPESA client. 

	The Mpesa Client will access all interactions with the MPESA Daraja API.
	"""

	auth_token = ''

	def __init__(self):
		"""
		The constructor for MpesaClient class
		"""

	def access_token(self):
		"""
		Generate an OAuth access token.

		Returns:
			bool: A string containg a valid OAuth access token
		"""
		
		return mpesa_access_token()

	def parse_stk_result(self, result):
		"""
		Parse the result of Lipa na MPESA Online Payment (STK Push)

		Returns:
			The result data as an array
		"""
		
		payload = json.loads(result)
		data = {}
		callback = payload['Body']['stkCallback']
		data['ResultCode'] = callback['ResultCode']
		data['ResultDesc'] = callback['ResultDesc']
		data['MerchantRequestID'] = callback['MerchantRequestID']
		data['CheckoutRequestID'] = callback['CheckoutRequestID']
		metadata = callback.get('CallbackMetadata')
		if metadata:
			metadata_items = metadata.get('Item')
			for item in metadata_items:
				data[item['Name']] = item.get('Value')
		
		return data

	def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
		"""
		Attempt to send an STK prompt to customer phone

		Args:
			phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
			amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
			account_reference (str) -- This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type. Along with the business name, this value is also displayed to the customer in the STK Pin Prompt message. Maximum of 12 characters.
			transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
			call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.

		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response
		
		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
		"""

		if str(account_reference).strip() == '':
			raise MpesaInvalidParameterException('Account reference cannot be blank')
		if str(transaction_desc).strip() == '':
			raise MpesaInvalidParameterException('Transaction description cannot be blank')
		if not isinstance(amount, int):
			raise MpesaInvalidParameterException('Amount must be an integer')


		phone_number = format_phone_number(phone_number)
		url = api_base_url() + 'mpesa/stkpush/v1/processrequest'
		passkey = mpesa_config('MPESA_PASSKEY')
		
		mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')
		if mpesa_environment == 'sandbox':
			business_short_code = mpesa_config('MPESA_EXPRESS_SHORTCODE')
		else:
			business_short_code = mpesa_config('MPESA_SHORTCODE')

		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		password = base64.b64encode((business_short_code + passkey + timestamp).encode('ascii')).decode('utf-8') 
		transaction_type = 'CustomerPayBillOnline'
		party_a = phone_number
		party_b = business_short_code

		data = {
			'BusinessShortCode': business_short_code,
			'Password': password,
			'Timestamp': timestamp,
			'TransactionType': transaction_type,
			'Amount': amount,
			'PartyA': party_a,
			'PartyB': party_b,
			'PhoneNumber': phone_number,
			'CallBackURL': callback_url,
			'AccountReference': account_reference,
			'TransactionDesc': transaction_desc
		}

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))

	def b2c_payment(self, phone_number, amount, transaction_desc, callback_url, occassion, command_id):
		"""
		Attempt to perform a business payment transaction

		Args:
			phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
			amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
			transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
			call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
			occassion (str) -- Any additional information to be associated with the transaction.

		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response
		
		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
		"""

		if str(transaction_desc).strip() == '':
			raise MpesaInvalidParameterException('Transaction description cannot be blank')
		if not isinstance(amount, int):
			raise MpesaInvalidParameterException('Amount must be an integer')

		phone_number = format_phone_number(phone_number)
		url = api_base_url() + 'mpesa/b2c/v1/paymentrequest'

		business_short_code = mpesa_config('MPESA_SHORTCODE')

		party_a = business_short_code
		party_b = phone_number
		initiator_username = mpesa_config('MPESA_INITIATOR_USERNAME')
		initiator_security_credential = encrypt_security_credential(mpesa_config('MPESA_INITIATOR_SECURITY_CREDENTIAL'))

		data = {
			'InitiatorName': initiator_username,
			'SecurityCredential': initiator_security_credential,
			'CommandID': command_id,
			'Amount': amount,
			'PartyA': party_a,
			'PartyB': party_b,
			'Remarks': transaction_desc,
			'QueueTimeOutURL': callback_url,
			'ResultURL': callback_url,
			'Occassion':  occassion
		}

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))

	def business_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'BusinessPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)

	def salary_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'SalaryPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)

	def promotion_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'PromotionPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)
