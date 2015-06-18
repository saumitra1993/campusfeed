import webapp2
import logging
import json
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class PostImageUrl(webapp2.RequestHandler):
	"""docstring for ImageUrl"""	

	def get(self):
		channel_id = self.request.get('channel_id').strip()
		dict_={}
		dict_['post_url_post'] = blobstore.create_upload_url('/channels/' + channel_id + '/posts')
		self.response.write(json.dumps(dict_))
		
