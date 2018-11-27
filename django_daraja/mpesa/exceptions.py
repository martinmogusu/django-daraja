"""
Exceptions raised during usage of the MPESa API
"""

class MpesaError(Exception):
	"""
	Raised for a general error regarding the library
	"""

class IllegalPhoneNumberException(Exception):
	"""
	Raised when phone number is in illegal format.
	"""
	pass


class MpesaConnectionError(Exception):
	"""
	Raised when connection has an error
	"""
	pass

class MpesaConfigurationException(Exception):
	"""
	Raised when Mpesa environment variables are not configured properly
	"""
	pass

class MpesaInvalidParameterException(Exception):
	"""
	Raised when an an invalid parameter is passed in a function call
	
	Extends:
		Exception: Exception
	"""
	pass


