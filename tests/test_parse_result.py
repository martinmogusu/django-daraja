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

	def test_parse_stk_push_result_success(self):
		'''
		Test parse successful STK push result
		'''
		result = '{"Body":{"stkCallback":{"MerchantRequestID":"19918-3028728-2","CheckoutRequestID":"ws_CO_DMZ_264695293_11032019122104433","ResultCode":0,"ResultDesc":"The service request is processed successfully.","CallbackMetadata":{"Item":[{"Name":"Amount","Value":1.00},{"Name":"MpesaReceiptNumber","Value":"NCB9FJNAIT"},{"Name":"Balance"},{"Name":"TransactionDate","Value":20190311122121},{"Name":"PhoneNumber","Value":254719748260}]}}}}'
		data = self.cl.parse_stk_result(result)
		self.assertEqual(data.get('ResultDesc'), 'The service request is processed successfully.')


	def test_parse_stk_push_result_wrong_pin(self):
		'''
		Test parse STK push result with wrong user PIN
		'''
		result = '{"Body":{"stkCallback":{"MerchantRequestID":"14683-2472331-1","CheckoutRequestID":"ws_CO_DMZ_264800546_11032019141837240","ResultCode":2001,"ResultDesc":"[MpesaCB - ]The initiator information is invalid."}}}'
		data = self.cl.parse_stk_result(result)
		self.assertEqual(data.get('ResultDesc'), '[MpesaCB - ]The initiator information is invalid.')


	def test_parse_stk_push_result_cancelled(self):
		'''
		Test parse STK push result with request cancelled by user
		'''
		result = '{"Body":{"stkCallback":{"MerchantRequestID":"19919-3025233-1","CheckoutRequestID":"ws_CO_DMZ_401294732_11032019121308821","ResultCode":1032,"ResultDesc":"[STK_CB - ]Request cancelled by user"}}}'
		data = self.cl.parse_stk_result(result)
		self.assertEqual(data.get('ResultDesc'), '[STK_CB - ]Request cancelled by user')

	def test_parse_stk_push_result_timeout(self):
		'''
		Test parse STK push result after timeout
		'''
		result = '{"Body":{"stkCallback":{"MerchantRequestID":"19924-2088990-1","CheckoutRequestID":"ws_CO_DMZ_262987371_09032019203456095","ResultCode":1036,"ResultDesc":"[STK_CB - ]SMSC ACK timeout."}}}'
		data = self.cl.parse_stk_result(result)
		self.assertEqual(data.get('ResultDesc'), '[STK_CB - ]SMSC ACK timeout.')