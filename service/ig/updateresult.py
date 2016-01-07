import webapp2
import json
import logging
from datetime import datetime
from handlers.mail import send_email
from google.appengine.api import blobstore
from service._users.sessions import BaseHandler
from db.database import Events, EventMatches, EventStandings
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from operator import itemgetter
from service._users.authentication import get_password_hash, passwords_match
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import TaskRetryOptions

class UpdateResult(webapp2.RequestHandler):

	def post(self):
			
			
		
		self.response.set_status(200,"Awesome")
		dict_ = {}
		dict_['status'] = "SUCCESS"
		self.response.write(json.dumps(dict_))


			