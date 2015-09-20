__author__ = 'Saumitra'

import webapp2
import os
import logging

class LockHandler(webapp2.RequestHandler):
		def get(self):
			 
			self.response.write(open('templates/lock.html').read())