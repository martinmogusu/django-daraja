# -*- coding: utf-8 -*-
'''
Test STK Push
'''

from django.test import TestCase
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from django_daraja.mpesa.utils import *
from django_daraja.mpesa.exceptions import *

class MpesaStkPushTestCase(TestCase):

	cl = MpesaClient()

	def test_stk_push_success(self):
		'''
		Test successful STK push
		'''
		
		# Wait for a short while (to avoid SpikeArrest)
		sleep(5, 'STK push success')

		phone_number = config('LNM_PHONE_NUMBER')
		amount = 1
		account_reference = 'reference'
		transaction_desc = 'Description'
		callback_url = 'https://darajambili.herokuapp.com/express-payment'
		response = self.cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
		self.assertEqual(response.response_description, 'Success. Request accepted for processing')

	def test_stk_push_empty_reference(self):
		'''
		Test that STK push with empty account reference raises MpesaInvalidParameterException
		'''

		with self.assertRaises(MpesaInvalidParameterException):
			phone_number = config('LNM_PHONE_NUMBER')
			amount = 1
			account_reference = ''
			transaction_desc = 'Description'
			callback_url = 'https://darajambili.herokuapp.com/express-payment'
			response = self.cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

		
	def test_stk_push_empty_description(self):
		'''
		Test that STK push with empty description raises MpesaInvalidParameterException
		'''

		with self.assertRaises(MpesaInvalidParameterException):
			phone_number = config('LNM_PHONE_NUMBER')
			amount = 1000000
			account_reference = 'reference'
			transaction_desc = ''
			callback_url = 'https://darajambili.herokuapp.com/express-payment'
			response = self.cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

	def test_stk_push_invalid_amount(self):
		'''
		Test that STK push with empty description raises MpesaInvalidParameterException
		'''

		with self.assertRaises(MpesaInvalidParameterException):
			phone_number = config('LNM_PHONE_NUMBER')
			amount = 1.5
			account_reference = 'reference'
			transaction_desc = 'Description'
			callback_url = 'https://darajambili.herokuapp.com/express-payment'
			response = self.cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
