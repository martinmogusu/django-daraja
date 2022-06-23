![Daraja logo](logo.png "Daraja logo")

# django-daraja

This is a django library based on the Safaricom MPESA daraja API. This is a django library based on the Safaricom MPESA daraja API. Use it for a simplified experience, spend less time setting up...

[![Build Status](https://circleci.com/gh/martinmogusu/django-daraja.svg?style=shield)](https://circleci.com/gh/martinmogusu/django-daraja)
[![Documentation Status](https://readthedocs.org/projects/django-daraja/badge/?version=latest)](https://django-daraja.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/django-daraja.svg)](https://badge.fury.io/py/django-daraja)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-daraja.svg)

Read the full documentation at https://django-daraja.readthedocs.io

MPESA Daraja API documentation can be found at https://developer.safaricom.co.ke

## Installation

To install the package, run

```
$ pip install django_daraja
```

## Examples

### STK Push

An example, to send an STK push prompt to customer phone, then display response message

```python
    from django_daraja.mpesa.core import MpesaClient

    def index(request):
        cl = MpesaClient()
        phone_number = '0700111222'
        amount = 1
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        return HttpResponse(response)
```

On your browser, you will receive a message `Success. Request accepted for processing` on success of the STK push. You will also receive a notification on the callback endpoint (In this case the URL with the name `mpesa_stk_push_callback`), having the results of the STK push.

### B2C Payment

An example, to perform a BusinessPayment B2C (Business to Customer) transaction

```python
    from django_daraja.mpesa.core import MpesaClient

    def index(request):
        cl = MpesaClient()
        phone_number = '0700111222'
        amount = 1
        transaction_desc = 'Business Payment Description'
        occassion = 'Test business payment occassion'
        callback_url = request.build_absolute_uri(reverse('mpesa_business_payment_callback'))
        response = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
        return HttpResponse(response)

```

On your browser, you will receive a message `Accept the service request successfully.` on success of the transaction. You will also receive a notification on the callback endpoint (In this case the URL with the name `mpesa_business_payment_callback`), having the results of the Business Payment Transaction.

## Note

You need a callback URL connected to the internet to receive the asynchronous result. In case you don't have one you can head over to http://darajambili.herokuapp.com and grab a callback URL to test the result.

The full documentation of all supported API's can be found at http://django-daraja.readthedocs.io
