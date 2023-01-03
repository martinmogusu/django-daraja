# -*- coding: utf-8 -*-
'''
Test Business Payment
'''

from django.test import TestCase
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from django_daraja.mpesa.exceptions import MpesaInvalidParameterException

class MpesaB2CPaymentTestCase(TestCase):

	cl = MpesaClient()
	callback_url = 'https://api.darajambili.com/express-payment'
	success_description = 'Accept the service request successfully.'

	def test_business_payment_success(self):
		'''
		Test successful business payment
		'''

		phone_number = config('B2C_PHONE_NUMBER')
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		response = self.cl.business_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)
		self.assertEqual(response.response_description, self.success_description)

	def test_salary_payment_success(self):
		'''
		Test successful salary payment
		'''

		phone_number = config('B2C_PHONE_NUMBER')
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		response = self.cl.salary_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)
		self.assertEqual(response.response_description, self.success_description)

	def test_promotion_payment_success(self):
		'''
		Test successful promotion payment
		'''

		phone_number = config('B2C_PHONE_NUMBER')
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		response = self.cl.promotion_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)
		self.assertEqual(response.response_description, self.success_description)
				
	def test_business_payment_empty_description(self):
		'''
		Test that Business Payment with empty description raises MpesaInvalidParameterException
		'''

		with self.assertRaises(MpesaInvalidParameterException):
			phone_number = config('B2C_PHONE_NUMBER')
			amount = 1000000
			occassion = 'occassion'
			transaction_desc = ''
			self.cl.business_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)

	def test_business_payment_invalid_amount(self):
		'''
		Test that Business Payment with invalid amount raises MpesaInvalidParameterException
		'''

		with self.assertRaises(MpesaInvalidParameterException):
			phone_number = config('B2C_PHONE_NUMBER')
			amount = 1.5
			occassion = 'occassion'
			transaction_desc = 'Description'
			self.cl.business_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)
