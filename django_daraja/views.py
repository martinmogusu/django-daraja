# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import *

from datetime import datetime

cl = MpesaClient()

def index(request):

	return HttpResponse('Welcome to the home of daraja APIs')

def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)

def stk_push_success(request):
	phone_number = '0719748260'
	amount = '1'
	account_reference = 'ABC001'
	r = cl.stk_push(phone_number, amount, account_reference)
	return JsonResponse(r.json())
