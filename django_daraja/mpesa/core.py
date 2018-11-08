import requests
from requests.auth import HTTPDigestAuth
import base64
from datetime import datetime
import json
from .exceptions import *
from .utils import *
from decouple import config

class MpesaClient:
	'''
	This is the core MPESA client. 

	The Mpesa Client will access all interactions with the MPESA Daraja API.
	'''

	auth_token = ''

	def __init__(self):
		'''
		The constructor for MpesaClient class
		'''

	def access_token(self):
		return mpesa_access_token()

	def stk_push(self, phone_number, amount, account_reference, transaction_desc = 'Description'):
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
		callback_url = 'https://darajambili.herokuapp.com/express-payment'

		data = {
			'BusinessShortCode': business_short_code,
			  'Password': password,
			  'Timestamp': timestamp,
			  'TransactionType': transaction_type,
			  'Amount': '1',
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

		print('Password: ', password)
		print('Password: ', password)

		try:
			r = requests.post(url, json=data, headers=headers)
			return r
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception:
			return ex.message

