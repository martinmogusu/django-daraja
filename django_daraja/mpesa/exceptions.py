'''
Exceptions raised during usage of the MPESa API
'''

class IllegalPhoneNumberException(Exception):
	'''
	Raised when phone number is in illegal format.
	'''
	pass


class MpesaConnectionError(Exception):
	'''
	Raised when connection has an error
	'''
	pass

class MpesaConfigurationException(Exception):
	'''
	Raised when Mpesa environment variables are not configured properly
	'''
	pass