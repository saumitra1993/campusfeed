__author__ = 'Saumitra'

import webapp2
import os
import logging
import json
from service._users.sessions import BaseHandler
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class PostUploadURL(BaseHandler, webapp2.RequestHandler):
    def get(self):
    	_dict = {}
    	channel_id = self.request.get('channel_id')
    	url = '/channels/'+ channel_id + '/posts'
    	_dict['upload_url'] = blobstore.create_upload_url(url)
    	self.response.set_status(200,'Awesome')
    	self.response.write(json.dumps(_dict))