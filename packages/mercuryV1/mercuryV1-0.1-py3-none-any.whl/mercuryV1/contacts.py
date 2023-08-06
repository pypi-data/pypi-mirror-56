from .base import Base

class Contacts(Base):
	""" Contacts class for handling the contact entity
	
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
		the base url including the token and a contacts extension
	extension : string
		an empty string for this class
	nestedEntity : boolean
		False for this class
	"""

	def __init__(self, url, token, headers):
		Base.__init__(self, url, token, headers)
		self.url += "/contacts"
		self.nestedEntity = False
		self.extension = ""

	def get(self, count=None, offset=0, search=None, sort=None):
		""" Method for searching and retrieving a list of contacts

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
			Contact name to search for
		isDeleted : boolean
			Set to true if searching for deleted contacts
		excludeDoNotMail : boolean
			Exclude contacts marked as do not email from the search results.
			If not set, will default to false
		excludeEmailBounced : boolean
			Exclude contacts with bounced emails from the search results. 
			If not passed, will default to false
		lastUpdated : string (yyyy-mm-dd)
			Returns results after the given lastUpdated date. Date should be in yyyy-mm-dd format
		companyName : string
			Company name of the person
		personType : string
			The relationship type of the person
		categoryId : string
			Search by the category id
		campaignId : string
			Search by the campaign id
		contactNumber : string
			Search by the contact number of the person
		email : string
			Search by the email address of the person
		dateOfBirth : string (yyyy-mm-dd)
			Search by date of birth of the person. Date should be in yyyy-mm-dd format
		birthday : string (yyyy-mm-dd)
			Search by birthday anniversary. Date should be in yyyy-mm-dd format
		createdOn : string (yyyy-mm-dd)
			Search by creation date. Date should be in yyyy-mm-dd format

		Sort Options
		------------
		key : string
			creationDate or lastModifiedDate. creationDate is default
		order : string
			ASC or DESC. DESC is default

		Raises
		------
		Exception
			Raised if the response returns an error.

		Returns
		-------
		list
		    a list of contacts in the form of dictionaries.
		    If search result returns no results, this method will return an empty list
		"""

		return super(Contacts, self).get(count=count, offset=offset, search=search, sort=sort)
		
	def create(self, data):
		""" Method for creating contacts

		Parameters
		----------
		data : dict
		    The data to be used to create the new contact
			
		Returns
		-------
		dict
		    the unique id of the newly created contact.
		"""
		return super(Contacts, self).create(data=data, id="")

	def fetch(self, id):
		""" Method for fetching contacts

		Parameters
		----------
		id : string
		    The unique id of the contact that is to be retrieved.

		Returns
		-------
		list
		    returns a list containing the contact.
		"""
		return super(Contacts, self).fetch(id=id)

	def update(self, id, data):
		""" Method for updating contacts

		Parameters
		----------
		id : string
		    The unique id of the contact that is to be updated.
		data : dict
		    The data to be used to update the contact

		Returns
		-------
		Response status code
			200 if successful
		"""
		return super(Contacts, self).update(id=id, data=data, nestedId="")

	def delete(self, id):
		""" Method for deleting contacts

		Parameters
		----------
		id : string
		    The unique id of the contact that is to be deleted.

		Returns
		-------
		Response status code
			200 if successful
		"""
		return super(Contacts, self).update(id=id, data={"isDeleted":True}, nestedId="")