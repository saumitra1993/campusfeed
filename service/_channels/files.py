import webapp2
import logging
import json
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):
        if not blobstore.get(file_key):
            self.error(404)
        else:
            self.send_blob(file_key)