__author__ = 'Saumitra'

import webapp2
import os
import logging

class Home(webapp2.RequestHandler):
		def get(self):
			 
			self.response.write(open('html/index.html').read())