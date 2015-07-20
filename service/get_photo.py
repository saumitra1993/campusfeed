import webapp2
import urllib
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
import logging

class GetPhotu(webapp2.RequestHandler):
	def get(self, img_id):
		entity_key = ndb.Key(urlsafe=img_id)
		entity = entity_key.get()
		if entity.img != '':
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(entity.img)
		else:
			self.response.out.write('No image')