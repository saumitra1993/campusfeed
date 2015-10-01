import webapp2
import logging
import json
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, file_key):
		if not blobstore.get(file_key):
			self.error(404)
		else:
			blob_info= blobstore.BlobInfo.get(file_key)
			file_name = blob_info.filename
			logging.info(file_name)
			self.response.headers["Content-Disposition"] = str("attachment; filename=" +file_name)
			self.send_blob(file_key)