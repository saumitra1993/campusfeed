__author__ = 'Saumitra'

import webapp2
import os
import logging

class WebHome(webapp2.RequestHandler):
		def get(self):
			 
				self.response.write(open('static/html/webhome.html').read())