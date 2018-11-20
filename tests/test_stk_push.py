# -*- coding: utf-8 -*-
'''
Test STK Push
'''

from django.test import TestCase
from django_daraja.mpesa.core import MpesaClient
from decouple import config

class MpesaStkPushTestCase(TestCase):

	cl = MpesaClient()

	def test_stk_push_success(self):
		'''
		Test successful STK push
		'''

		phone_number = config('LNM_PHONE_NUMBER')
		amount = 1
		account_reference = 'reference'
		transaction_desc = 'Description'
		callback_url = 'https://darajambili.herokuapp.com/express-payment'
		response = self.cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
		self.assertEqual(response.response_description, 'Success. Request accepted for processing')

		
