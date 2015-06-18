import webapp2
import logging
import json
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ImageUrl(webapp2.RequestHandler):
	"""docstring for ImageUrl"""	

	def get(self):
		dict_={}
		dict_['post_url'] = blobstore.create_upload_url('/login')
		self.response.write(json.dumps(dict_))
		
