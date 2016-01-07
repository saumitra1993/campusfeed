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

class EventTime(webapp2.RequestHandler):

	def post(self):

		event_code = self.request.get('event_id')
		time_string = self.request.get('time')
		event_type = self.request.get('event_type')
		location = self.request.get('location')
		match_type = self.request.get('match_type')
		dept1_code = self.request.get('dept1')
		dept2_code = self.request.get('dept2')

		if event_type == 'tournament' and match_type == 'qf':
			


		self.response.set_status(200,"Awesome")
		dict_ = {}
		dict_['status'] = "SUCCESS"
		self.response.write(json.dumps(dict_))


			