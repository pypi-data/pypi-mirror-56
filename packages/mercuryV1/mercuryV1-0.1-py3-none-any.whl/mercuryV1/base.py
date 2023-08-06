import json
import requests


class Base():
	""" Base class for handling all requests to the API
	
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
		the base url including the token.
	headers : dict
		dictionary with required headers for making requests, contains the API key
	"""

	def __init__(self, url, token, headers):
		self.url = url+token
		self.headers = headers

	def __urlGenerate(self, id, nestedId=""):
		""" Helper method for generating request urls

		Parameters
		----------
		id : string
		    The unique ID of the entity
		nestedId : string, optional
		    The unique ID of the nested entity.
		Returns
		-------
		string
		    the url to be used to make an API request.
		"""

		url = self.url
		if not self.nestedEntity:
			url += "/"
		return "{url}{id}{extension}{nestedId}".format(url=url, id=id, extension=self.extension, 
			nestedId=nestedId)

	def get(self, count=None, offset=0, search=None, sort=None):
		""" Base method for searching and retrieving contacts and opportunities

		Parameters
		----------
		count : int, optional
			The number of search results to return
		offset : int, optional
			Will return search results after the offset number
		search : dict, optional
			A list of parameters to search by.
			See contacts or opportunities class for specific details
		sort : dict, optional
			A list of options to modify the sorting of the results.
			Can sort by creationDate or lastModifiedDate and sort ascending or
			descending.
			See below 'Sort Options' for details

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
			a list of entities in the form of dictionaries.
			if search result returns no results, this method will return an empty list
		"""

		parameters = {
			'count':100,
			'offset':offset,
			'sortKey':"creationDate",
			'sortOrder':"DESC"}

		if sort:
			if 'key' in sort:
				parameters['sortKey'] = sort['key']
			if 'order' in sort:
				parameters['sortOrder'] = sort['order']

		if search:
			parameters['searchParams'] = json.dumps(search)

		result = list()
		# retrieve entities between start and end
		start = offset
		end = 100+offset

		if count:
			# if a count is provided in the parameters, change the default 100 to the count provided
			end = count+offset

		while start < end:
			parameters['offset'] = start
			parameters['count'] = min(end-start, 100)
			url = requests.Request('GET',
				url=self.url+"?search",
				params=parameters, 
				).prepare().url
			response = requests.get(url, headers=self.headers).json()
			
			if 'results' not in response:
				# if there is a problem with the request, raise an exception and display the result
				raise Exception("There was a problem with your request",response['errorMessage'])

			if response['totalCount'] == 0:
				# if search returns no result, return empty list
				return list()

			if not count:
				# if no count was provided in the parameters, the count needs to be updated to reflect the
				# total number of results that can be returned.
				end = response['totalCount']

			# update results and start counter
			result.extend(response['results'])
			start += len(response['results'])
		return result


	def create(self, data, id=""):
		""" Base method for creating entities

		Parameters
		----------
		data : dict
		    The data to be used to create the new entity
		id : string, optional
			Used only for nested entities.
		    If a nested entity, the id will be used to attach the new entity to the contact or opportunity

		Returns
		-------
		dict
		    the unique id of the newly created entity.
		"""

		return requests.post(self.__urlGenerate(id),
			headers=self.headers,
			data=json.dumps(data)
			).json()

	def fetch(self, id):
		""" Base method for fetching entities

		Parameters
		----------
		id : string
		    The unique id of the entity that is to be retrieved.

		Returns
		-------
		list
		    If the entity fetched is an opportunity or contact, then this will be returned. Otherwise, if a nested entity was requested,
		    then passing the parent contact or opportunity unique id will return a list of all nested entities in the parent entity. 
		"""

		return requests.get(
			self.__urlGenerate(id), 
			headers=self.headers
			).json()

	def update(self, id, data, nestedId=""):
		""" Base method for updating entities

		Parameters
		----------
		id : string
		    The unique id of the entity that is to be updated.
		data : dict
		    The data to be used to update the entity
		nestedId : string, optional
			Used only for nested entities.
		    The unique id of the nested entity that will be updated.

		Returns
		-------
		Response status code
			200 if successful
		"""

		return requests.put(
			self.__urlGenerate(id,nestedId), 
			headers=self.headers, 
			data=json.dumps(data)
			)