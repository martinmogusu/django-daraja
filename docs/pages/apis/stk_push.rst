STK Push API
============

The STK Push API is used to push a prompt to a customer's phone, asking the customer to enter a PIN. 

This simplifies the process of C2B payments, since the business can specify all the necessary parameters for the payment (e.g. amount, shortcode e.t.c), so that the customer will just enter their MPESA PIN to authorize the payment.

Example:

	..	code-block:: python

		from django_daraja.mpesa.core import MpesaClient

		phone_number = '07xxxxxxxx'
		amount = 1
		account_reference = 'reference'
		transaction_desc = 'Description'
		callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
		response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

This will assign the ``response`` variable with an ``MpesaResponse`` object containing the response returned from the STK Push API call. 

.. note::
	- Use a Safaricom number that you have access to for the ``phone_number`` parameter, so as to be able to receive the prompt on your phone.
	- You will need to define a url with the name ``mpesa_stk_push_callback``, and this is where MPESA will send the results of the STK push once the customer enters the PIN or cancels the transaction, or in case the prompt times out.
	- This example will work if your site is already hosted, since the callback URL needs to be accessible via internet. For local testing purposes, you can use an endpoint hosted outside your site to check the notification received on the callback URL. There is a test listener hosted at https://darajambili.herokuapp.com, which you can use to view logs of notifications received. You can head over there to pick a callback URL to use for STK push.