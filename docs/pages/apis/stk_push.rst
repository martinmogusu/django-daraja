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
		callback_url = 'https://api.darajambili.com/express-payment'
		response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

This will assign the ``response`` variable with an ``MpesaResponse`` object containing the response returned from the STK Push API call. 

.. note::
	- Use a Safaricom number that you have access to for the ``phone_number`` parameter, so as to be able to receive the M-PESA prompt on your phone.
	- Once you have entered the PIN, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/express-payment), you can head over to https://darajambili.com to view the notification received.