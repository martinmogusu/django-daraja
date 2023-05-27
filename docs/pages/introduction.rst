Introduction
============
This is a django library to interact with the Safaricom MPESA Daraja API (https://developer.safaricom.co.ke)

The source code can be found at https://github.com/martinmogusu/django-daraja.git

Installation
------------

To install the package, run

    ..	code-block:: none

        $ pip install django_daraja

Example
--------------

An example, to send an STK push prompt to customer phone, then display response message

    ..	code-block:: python
    	:caption: views.py
    	:name: views.py

        from django_daraja.mpesa.core import MpesaClient
        
        def index(request):
            cl = MpesaClient()
            phone_number = '0700111222'
            amount = 1
            account_reference = 'reference'
            transaction_desc = 'Description'
            callback_url = 'https://api.darajambili.com/express-payment'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response)

On your browser, you will receive the API response message and on the phone number specified you will receive an MPESA PIN prompt. Once you have entered the PIN, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/express-payment), you can head over to https://darajambili.com to view the notification received.