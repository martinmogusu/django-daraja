Quick Start Guide
=================
This is a quick start guide on seting up a simple project and implement some features of the django-daraja library.

1. Install
----------

To install the package, run

    .. code-block:: none

        $ pip install django_daraja

2. Create a django project
--------------------------

Run this code to create  a django project

    .. code-block:: none

        $ django-admin startproject my_site
        $ cd my_site
        $ django-admin startapp my_app

3. Environment Configuration
----------------------------

Create a ``.env`` file in the root folder (``my_site``) and in the file load the configuration for your daraja developer app. Fill it in with these details:

    .. code-block:: none
       :caption: .env
       :name: .env

        # MPESA Configuration variables     
                
        # The Mpesa environment to use
        # Possible values: sandbox, production
        
        MPESA_ENVIRONMENT=sandbox        
        
        # Credentials for the daraja app
        
        MPESA_CONSUMER_KEY=mpesa_consumer_key
        MPESA_CONSUMER_SECRET=mpesa_consumer_secret
        
        
        #Shortcode to use for transactions
        
        MPESA_SHORTCODE=mpesa_shortcode
        
        
        # Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
        # This only has a different value on sandbox, you do not need to set it on production
        
        MPESA_EXPRESS_SHORTCODE=mpesa_express_shortcode        
        
        #Type of shortcode
        # Possible values: 
        # - paybill (For Paybill)
        # - till_number (For Buy Goods Till Number)
        
        MPESA_SHORTCODE_TYPE=paybill
        
        # Lipa na MPESA Online passkey
        # Sandbox passkey is available on test credentials page
        # Production passkey is sent via email once you go live
        
        MPESA_PASSKEY=mpesa_passkey

Alternatively, in ``settings.py`` you can add the environment configuration as settings variables. (This is not very recommended since you will most likely NOT want to have configuration settings - e.g. consumer keys/secrets - as part of your commits.)

4 Settings configuration
------------------------

In ``settings.py``, add ``django_daraja`` to the ``INSTALLED_APPS`` list

    .. code-block:: python
       :caption: settings.py
       :name: settings.py

        INSTALLED_APPS = [
            ...,
            'django.contrib.staticfiles',
            'django_daraja',
            'my_app',
        ]

5. URL Configuration
--------------------

In ``urls.py``, Add the URL configuration

Python 2:
    .. code-block:: python

        from django.conf.urls import url, include
        from django.contrib import admin

        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^daraja/', include('django_daraja.urls')),
        ]

Python 3:
    .. code-block:: python

        from django.contrib import admin
        from django.urls import path, include
        
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('my_app.urls')),
        ]

In ``my_app/urls.py`` Add this code to create a test endpoint

Python 2:
    .. code-block:: python
       
        from django.conf.urls import url, include
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
        ]

Python 3:
    .. code-block:: python

        from django.urls import path, include
        from . import views
        urlpatterns = [
            path('', views.index, name='index'),
        ]

6. Create a view
----------------

In ``my_app/views.py`` Create a test index view

    .. code-block:: python

        from django.shortcuts import render
        from django.http import HttpResponse
        from django_daraja.mpesa.core import MpesaClient
        
        def index(request):
            cl = MpesaClient()
            # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
            phone_number = 'PHONE_NUMBER'
            amount = 1
            account_reference = 'reference'
            transaction_desc = 'Description'
            # This is a test callback URL.
            # You can replace this with an endpoint where you wish to receive the result of the STK push transaction.
            callback_url = 'https://darajambili.herokuapp.com/express-payment'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response.text)

7. Run Migrations
-----------------

On the command line, run migrations to add the models created by the library

    .. code-block:: none

        $ python manage.py migrate

8. Run the server
-----------------

Then run the server
    .. code-block:: none

        $ python manage.py runserver

You can now visit your site at ``localhost:8000`` to view your project

If the STK push was successful, you should see an STK prompt on your phone (the phone number you provided), and you should see the response on the browser. It looks like this:

   .. code-block:: json

        {
            "MerchantRequestID": "2134-9231241-1",
            "CheckoutRequestID": "ws_CO_DMZ_157917982_20112018173133556",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing"
        }
