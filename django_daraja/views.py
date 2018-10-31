# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

class MpesaCoreView(View):

	def get(self, request):
		return HttpResponse(10)