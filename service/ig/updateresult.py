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
			
		distribution_type = self.request.get('distribution_type')
		event_code = self.request.get('event_id')
		winner_id = self.request.get('winner_id')
		loser_id = self.request.get('loser_id')
		points = self.request.get('points')
		message = self.request.get('message')
		dept_positions = self.request.get('dept_positions')
		position_points = self.request.get('position_points')
		
		result3 = Events.query(Events.code == event_code).fetch()
		if len(result1) == 1 and len(result2) == 1 and len(result3) == 1:
			if distribution_type == 'per_match':
				result1 = Departments.query(Departments.dept1_code == winner_id).fetch()
				result2 = Departments.query(Departments.dept2_code == loser_id).fetch()
		self.response.set_status(200,"Awesome")
		dict_ = {}
		dict_['status'] = "SUCCESS"
		self.response.write(json.dumps(dict_))


			