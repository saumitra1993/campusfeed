import webapp2
import logging
import json
from db.database import Users
from google.appengine.ext import ndb
from google.appengine.api import search

class SearchChannels(webapp2.RequestHandler):
	"""docstring for SearchChannels"""
	
	# Request URL: /channels/search?search_string=search_query GET
	# Response: results: dict(array of(first_name,last_name,user_id,user_img_url,branch))
	# DATA IN DATABASE IS ALWAYS COMPLETELY LOWERCASE
	def get(self):

		search_string = self.request.get('search_string').strip() #search_string is a name(first/last)
		dict_={}
		try:
		  index = search.Index("channelsearch")
		  search_results = index.search(search_string)

		  out = []
		  for doc in search_results:
			doc_id = doc.doc_id
			fields = doc.fields
			_dict = {}
			_dict['channel_id'] = doc_id
			_dict['channel_name'] = fields[0].value
			_dict['description'] = fields[1].value
			out.append(_dict)
		except search.Error:
			logging.error("Error!")
			
		dict_['results'] = out
		self.response.write(json.dumps(dict_))