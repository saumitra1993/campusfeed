__author__ = 'Saumitra'

import webapp2
import os
import logging

class GuestHandler(webapp2.RequestHandler):
		def get(self):
			 
			self.response.write(open('templates/guest_channel.html').read())