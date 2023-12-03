OAuth API
============

The OAUth API is used to generate an access token, which is used for authentication in all the other APIs.

.. note::
	Functionality for the OAUth API has been automated in the django-daraja; the library will automatically generate an access token before making an API call and attach it to the request headers of the API call. Access tokens expire after an hour, so this library stores the access token for a maximum of 50 minutes to avoid repeated calls to the OAuth endpoint.

You can test the OAuth API by using the ``MpesaClient.access_token`` method

	..	code-block:: python

		from django_daraja.mpesa.core import MpesaClient

		cl = MpesaClient()
		token = cl.access_token()

This will assign the ``token`` variable with an access token generated from the OAuth endpoint, or stored locally if available. 
