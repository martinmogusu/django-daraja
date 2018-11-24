Introduction
============
This is a django library to interact with the Safaricom MPESA Daraja API (https://developer.safaricom.co.ke)

Download the source	code at https://github.com/martinmogusu/django-daraja.git

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
            callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response.response_description)

On your browser, you will receive a message ``Success. Request accepted for processing`` on success of the STK push. You will also receive a notification on the callback endpoint (In this case the URL with the name ``mpesa_stk_push_callback``), having the results of the STK push.