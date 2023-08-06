from .nestedBase import NestedBase

class Liabilities(NestedBase):
	""" Liabilities class for handling the liability entity
	
	Parameters
	----------
	url : string
		the base url used for making requests to the API, either the sandbox or production URL
	token : string
		the token required for making requests, found in mercury
	headers : dict
		a dictionary with required headers for making requests. Contains the API key, found in mercury
	"""

	def __init__(self, url, token, headers):
		NestedBase.__init__(self, url, token, headers, "opportunities", "liabilities")

	def get(self):
		"""
			'Liabilities' object has no attribute 'get'
		"""
		raise AttributeError( "'Liabilities' object has no attribute 'get'" )

	def fetch(self):
		"""
			'Liabilities' object has no attribute 'fetch'
		"""
		raise AttributeError( "'Liabilities' object has no attribute 'fetch'" )