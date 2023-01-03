B2C Payment APIs
================

The B2C Payment APIs are used to make Business to Customer payments. Currently 3 transactions are supported in this model:

Business Payment
  This is a normal business to customer payment,  supports only M-Pesa registered customers.

Salary Payment
  This supports sending money to both registere and unregistered M-Pesa customers.

Promotion Payment
  This is a promotional payment to customers. The M-Pesa notification message is a congratulatory message. Supports only M-Pesa registered customers.

Examples:

Business Payment
----------------

	..	code-block:: python

		from django_daraja.mpesa.core import MpesaClient

		phone_number = '07xxxxxxxx'
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		callback_url = 'https://api.darajambili.com/b2c/result'
		response = self.cl.business_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)

Salary Payment
----------------

	..	code-block:: python

		from django_daraja.mpesa.core import MpesaClient

		phone_number = '07xxxxxxxx'
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		callback_url = 'https://api.darajambili.com/b2c/result'
		response = self.cl.business_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)

Promotion Payment
----------------

	..	code-block:: python

		from django_daraja.mpesa.core import MpesaClient

		phone_number = '07xxxxxxxx'
		amount = 1
		transaction_desc = 'Description'
		occassion = 'Occassion'
		callback_url = 'https://api.darajambili.com/b2c/result'
		response = self.cl.promotion_payment(phone_number, amount, transaction_desc, self.callback_url, occassion)


This will assign the ``response`` variable with an ``MpesaResponse`` object containing the response returned from the Business Payment B2C API Call 

.. note::
	- Test credentials to use for this scenario can be found at the developer portal (https://developer.safaricom.co.ke/test_credentials)
	- Use `shortcode 1` as the shortcode, and the test MSISDN as the B2C phone number
	- Once the transaction is complete, you will receive a notification on the callback URL you provided. If you used the exact callback URL in the example above (i.e. https://api.darajambili.com/b2c/result), you can head over to https://darajambili.com to view the notification received