# -*- coding: utf-8 -*-
'''
Test Business Payment
'''

from django.test import TestCase
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from django_daraja.mpesa.exceptions import MpesaInvalidParameterException
from django_daraja.mpesa.utils import sleep

class MpesaB2CPaymentTestCase(TestCase):

	cl = MpesaClient()
	callback_url = 'https://darajambili.herokuapp.com/express-payment'
	success_description = 'Accept the service request successfully.'

	def test_business_payment_success(self):
		'''
		Test successful business payment
		'''

		# Wait for a short while (to avoid SpikeArrest)
		sleep(20, 'Test business payment success')

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
		
		# Wait for a short while (to avoid SpikeArrest)
		sleep(20, 'Test salary payment success')

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

		# Wait for a short while (to avoid SpikeArrest)
		sleep(20, 'Test promotion payment success')

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
