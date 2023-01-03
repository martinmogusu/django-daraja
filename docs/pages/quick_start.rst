Quick Start Guide
=================
This is a quick start guide on seting up a simple project and implement some features of the django-daraja library.

1. Install
----------

To install the package, run

    ..	code-block:: none

        $ pip install django_daraja

2. Create a django project
--------------------------

Run these commands to create  a django project

    ..	code-block:: none

        $ django-admin startproject my_site
        $ cd my_site
        $ django-admin startapp my_app

3. Create a developer app
-------------------------

Head to https://developer.safaricom.co.ke and create a developer account, log in and create an app. You will use the **Consumer Key** and **Consumer Secret** of this app, as well as the **test credentials** assigned to you for the next step. 

4. Environment Configuration
----------------------------

	.. hint::
		Test credentials (for sandbox testing) can be found at https://developer.safaricom.co.ke/test_credentials.

Add the details below at the bottom of your `settings.py` file

	.. warning::
		Adding sensitive configuration in the settings file is not recommended on production since you will most likely NOT want to have configuration settings - e.g. consumer keys/secrets - as part of your code, which will be added to version control. It is recommended to use a .env file and a library like `python-decouple` so that the configuration can be externalized when deploying to production

    ..	code-block:: python
    	:caption: my_site/settings.py
    	:name: my_site_settings

        # The Mpesa environment to use
        # Possible values: sandbox, production

        MPESA_ENVIRONMENT = 'sandbox'

        # Credentials for the daraja app

        MPESA_CONSUMER_KEY = 'mpesa_consumer_key'
        MPESA_CONSUMER_SECRET = 'mpesa_consumer_secret'

        #Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

        MPESA_SHORTCODE = 'mpesa_shortcode'

        # Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
        # This is only used on sandbox, do not set this variable in production
        # For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

        MPESA_EXPRESS_SHORTCODE = 'mpesa_express_shortcode'

        # Type of shortcode
        # Possible values: 
        # - paybill (For Paybill)
        # - till_number (For Buy Goods Till Number)

        MPESA_SHORTCODE_TYPE = 'paybill'

        # Lipa na MPESA Online passkey
        # Sandbox passkey is available on test credentials page
        # Production passkey is sent via email once you go live

        MPESA_PASSKEY = 'mpesa_passkey'

        # Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

        MPESA_INITIATOR_USERNAME = 'initiator_username'

        # Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

        MPESA_INITIATOR_SECURITY_CREDENTIAL = 'initiator_security_credential'


5. Settings configuration
-------------------------

In ``settings.py``, add ``django_daraja``  and ``my_app`` to the ``INSTALLED_APPS`` list

    ..	code-block:: python
    	:caption: my_site/settings.py
    	:name: settings_installed_apps

        INSTALLED_APPS = [
            ...,
            'django_daraja',
            'my_app',
        ]

6. URL Configuration
--------------------

In ``urls.py``, Add the URL configuration

Python 2:
    ..	code-block:: python
    	:caption: my_site/urls.py
    	:name: urls_python_2

        from django.urls import re_path as url, include
        from django.contrib import admin

        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^', include('my_app.urls')),
        ]

Python 3:
    ..	code-block:: python
    	:caption: my_site/urls.py
    	:name: urls_python_3

        from django.urls import path, include
        from django.contrib import admin
        
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('my_app.urls')),
        ]

In ``my_app/urls.py``, add the code to create a home page, as well as the endpoint to receive notifications from MPESA

Python 2:
    ..	code-block:: python
    	:caption: my_app/urls.py
    	:name: my_app_urls_python_2
       
        from django.urls import re_path as url

        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index')
        ]

Python 3:
    ..	code-block:: python
    	:caption: my_app/urls.py
    	:name: my_app_urls_python_3

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index')
        ]

7. Create a view
----------------

In ``my_app/views.py`` Create a test index view

    ..	code-block:: python
    	:caption: my_app/views.py
    	:name: my_app_views

        from django.shortcuts import render
        from django.http import HttpResponse
        from django_daraja.mpesa.core import MpesaClient
        
        def index(request):
            cl = MpesaClient()
            # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
            phone_number = '07xxxxxxxx'
            amount = 1
            account_reference = 'reference'
            transaction_desc = 'Description'
            callback_url = 'https://api.darajambili.com/express-payment'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response)

.. note::
	- Use a Safaricom number that you have access to for the ``phone_number`` parameter, so as to be able to receive the M-PESA prompt on your phone.
    - Once you have entered the PIN, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/express-payment), you can head over to https://darajambili.com to view the notification received.

8. Run Migrations
-----------------

On the command line, run migrations to add the models created by the library

    ..	code-block:: none

        $ python manage.py migrate

9. Run the server
-----------------

Then run the server

    ..	code-block:: none

        $ python manage.py runserver

You can now visit your site at ``localhost:8000`` to view your project

If the STK push was successful, you should see an STK prompt on your phone (the phone number you provided), and you should see the response on the browser. It looks like this:

   ..	code-block:: json

        {
            "MerchantRequestID": "2134-9231241-1",
            "CheckoutRequestID": "ws_CO_DMZ_157917982_20112018173133556",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing"
        }

You will also receive a notification on the callback endpoint that you specified having the results of the STK push.