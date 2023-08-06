from .contacts import Contacts
from .opportunities import Opportunities
from .addresses import Addresses
from .contactMethods import ContactMethods
from .expenses import Expenses
from .incomes import Incomes
from .assets import Assets
from .liabilities import Liabilities
from .relatedParties import RelatedParties

class Mercury():
	""" The central class of the API - it is used to make connections with mercury.
		For more information visit https://support.connective.com.au/hc/en-us/articles/360009453654-Getting-Started-with-Mercury-API

	Parameters
	----------
	token : string
		the token required for making requests, found in mercury
	key : string
		the key required for making requests, found in mercury
	sandbox : boolean
		to indicate whether to use the UAT url or production url.
		*the token will be different for UAT and production, however the key will remain the same
	Attributes
	----------
	url : string
		the base url for making requests.
	headers : dict
		dictionary with required headers for making requests, contains the API key
	token : dict
		the token required for making requests
	"""

	def __init__(self, token, key, sandbox=False):
		self.headers = { 'x-api-key' : key }
		self.token = token

		if sandbox:
			self.url = "https://uatapis.connective.com.au/mercury-v1/"
		else:
			self.url = "https://apis.connective.com.au/mercury/v1/"

		self.contacts = Contacts(url=self.url,token=self.token,headers=self.headers)
		self.addresses = Addresses(url=self.url,token=self.token,headers=self.headers)
		self.contactMethods = ContactMethods(url=self.url,token=self.token,headers=self.headers)
		self.incomes = Incomes(url=self.url,token=self.token,headers=self.headers)
		self.expenses = Expenses(url=self.url,token=self.token,headers=self.headers)
		self.opportunities = Opportunities(url=self.url,token=self.token,headers=self.headers)
		self.assets = Assets(url=self.url,token=self.token,headers=self.headers)
		self.liabilities = Liabilities(url=self.url,token=self.token,headers=self.headers)
		self.relatedParties = RelatedParties(url=self.url,token=self.token,headers=self.headers)
