# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase

class MpesaCoreTestCase(TestCase):

	def test_index_view(self):
		'''
		Test home page content
		'''
		
		response = self.client.get(reverse("django_daraja_index"))
		self.assertEqual(response.content, b"Welcome to the home of daraja APIs")