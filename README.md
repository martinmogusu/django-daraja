![Daraja logo](logo.png "Daraja logo")

# django-daraja

This is a django library based on the Safaricom MPESA daraja API. This is a django library based on the Safaricom MPESA daraja API. Use it for a simplified experience, spend less time setting up...

[![Build Status](https://travis-ci.org/martinmogusu/django-daraja.svg?branch=master)](https://travis-ci.org/martinmogusu/django-daraja)
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

## Example

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
        return HttpResponse(response.response_description)
```

On your browser, you will receive a message `Success. Request accepted for processing` on success of the STK push. You will also receive a notification on the callback endpoint (In this case the URL with the name `mpesa_stk_push_callback`), having the results of the STK push.