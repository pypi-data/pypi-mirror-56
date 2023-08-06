from .base import Base

class NestedBase(Base):
	""" Nested entity base class for handling requests to the API
	
	Parameters
	----------
	url : string
		the base url used for making requests to the API, either the sandbox or production URL
	token : string
		the token required for making requests, found in mercury
	headers : dict
		a dictionary with required headers for making requests. Contains the API key, found in mercury
	parent : string
		either 'opportunities' or 'contacts'
	extension : string
		the name of the nested entity for the url

	Attributes
	----------
	url : string
		the base url including the token.
	headers : dict
		dictionary with required headers for making requests, contains the API key
	nestedEntity : boolean
		True for this class
	nestedParent : string
		either 'opportunities' or 'contacts'
	extension : string
		the name of the nested entity for the url
	"""

	def __init__(self, url, token, headers, parent, extension):
		Base.__init__(self, url, token, headers)
		self.url += "/{}/".format(parent)
		self.nestedEntity = True
		self.nestedParent = parent
		self.extension = "/{}/".format(extension)

	def create(self, data, parentId):
		""" Method for creating nested entities

		Parameters
		----------
		data : dict
			The data to be used to create the new nested entity
		parentId : string
			The id of the opportunity or contact related to the nested entity
			
		Returns
		-------
		dict
			the unique id of the newly created nested entity.
		"""

		return Base.create(self, data=data, id=parentId)

	def update(self, data, parentId, nestedId):
		""" Method for updating nested entities

		Parameters
		----------
		data : dict
			The data to be used to create the new nested entity
		parentId : string
			The id of the opportunity or contact related to the nested entity
		nestedId : string
			The id of the nested entity to be updated.
			
		Returns
		-------
		Response status code
			200 if successful
		"""

		return Base.update(self, id=parentId,data=data,nestedId=nestedId)

	def delete(self, parentId, nestedId):
		""" Method for deleting nested entities

		Parameters
		----------
		parentId : string
			The id of the opportunity or contact related to the nested entity
		nestedId : string
			The id of the nested entity to be deleted.
			
		Returns
		-------
		Response status code
			200 if successful
		"""

		return Base.update(self, id=parentId, data={"isDeleted":True}, nestedId=nestedId)