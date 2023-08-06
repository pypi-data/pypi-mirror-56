from .base import Base

class Opportunities(Base):
	""" Opportunities class for handling the Opportunity entity
	
	Parameters
	----------
	url : string
		the base url used for making requests to the API, either the sandbox or production URL
	token : string
		the token required for making requests, found in mercury
	headers : dict
		a dictionary with required headers for making requests. Contains the API key, found in mercury
	Attributes
	----------
	url : string
		the base url including the token and a opportunities extension
	extension : string
		an empty string for this class
	nestedEntity : boolean
		False for this class
	"""

	def __init__(self, url, token, headers):
		Base.__init__(self, url, token, headers)
		self.url += "/opportunities"
		self.nestedEntity = False
		self.extension = ""

	def get(self, count=None, offset=0, search=None, sort=None):
		""" Method for searching and retrieving a list of opportunities

		Parameters
		----------
		count : int, optional
		    The number of search results to return
		offset : int, optional
		    Will return search results after the offset number
		search : dict, optional
		    A list of parameters to search by.
		    See below 'Search Options' for details.
		sort : dict, optional
			A list of options to modify the sorting of the results.
			Can sort by creationDate or lastModifiedDate and sort ascending or 
			descending.
			See below 'Sort Options' for details.

		Search Options
		--------------
		name : string
			Opportunity name to search for
		isDeleted : boolean
			Set to true if searching for deleted opportunities
		statuses : list 
			List of opportunity statuses
		lastUpdated	: string (yyyy-mm-dd)
			Search by last updated date. Date should be in yyyy-mm-dd format.
		transactionType : string
			The type of transaction
		user : string 
			CA number of the agent
		createdOn : string (yyyy-mm-dd)
			Search by created date. Date should be in yyyy-mm-dd format.
		confirmedSettlementDate : string (yyyy-mm-dd)
			Search by settlement date. Date should be in yyyy-mm-dd format.
		interestOnlyExpiry : string (yyyy-mm-dd)
			Search by interest only expiry date. Date should be in yyyy-mm-dd format.
		fixedRateExpiry : string (yyyy-mm-dd)
			Search by fixed rate expiry date. Date should be in yyyy-mm-dd format.

		Sort Options
		------------
		key
			creationDate or lastModifiedDate. creationDate is default
		order
			ASC or DESC. DESC is default

		Raises
		------
		Exception
			Raised if the response returns an error.

		Returns
		-------
		list
		    a list of opportunities in the form of dictionaries.
		    If search result returns no results, this method will return an empty list
		"""

		return super(Opportunities, self).get(count=count, offset=offset, search=search, sort=sort)
		
	def create(self, data):
		""" Method for creating opportunities

		Parameters
		----------
		data : dict
		    The data to be used to create the new opportunity
			
		Returns
		-------
		dict
		    the unique id of the newly created opportunity.
		"""
		return super(Opportunities, self).create(data=data, id="")

	def fetch(self, id):
		""" Method for fetching opportunities

		Parameters
		----------
		id : string
		    The unique id of the opportunity that is to be retrieved.

		Returns
		-------
		list
		    returns a list containing the opportunity.
		"""
		return super(Opportunities, self).fetch(id=id)

	def update(self, id, data):
		""" Method for updating opportunities

		Parameters
		----------
		id : string
		    The unique id of the opportunity that is to be updated.
		data : dict
		    The data to be used to update the opportunity

		Returns
		-------
		Response status code
			200 if successful
		"""
		return super(Opportunities, self).update(id=id, data=data, nestedId="")

	def delete(self, id):
		""" Method for deleting opportunities

		Parameters
		----------
		id : string
		    The unique id of the opportunity that is to be deleted.

		Returns
		-------
		Response status code
			200 if successful
		"""
		return super(Opportunities, self).update(id=id, data={"isDeleted":True}, nestedId="")