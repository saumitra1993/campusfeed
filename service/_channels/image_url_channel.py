import webapp2
import logging
import json
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ChannelImageUrl(webapp2.RequestHandler):
	"""docstring for ImageUrl"""	

	def get(self):
		dict_={}
		dict_['img_url_channel'] = blobstore.create_upload_url('/channels')
		self.response.write(json.dumps(dict_))
		
