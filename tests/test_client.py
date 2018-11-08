# -*- coding: utf-8 -*-
"""
Test the MPESA client
"""

from __future__ import unicode_literals
from django.urls import reverse
from django.test import TestCase
from django_daraja.mpesa.core import MpesaClient

class MpesaClientTestCase(TestCase):

	def test_client_init(self):
		'''
		Test initialization of MPESA Client
		'''
		
		cl = MpesaClient()
		self.assertEqual(cl.__class__.__name__, 'MpesaClient')

