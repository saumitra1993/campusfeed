from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
import urllib
import logging

class GetPhotu(blobstore_handlers.BlobstoreDownloadHandler):
   	def get(self, d_pic_id):
		resource = str(urllib.unquote(d_pic_id))
		blob_info = blobstore.BlobInfo.get(d_pic_id)
		self.send_blob(blob_info)
