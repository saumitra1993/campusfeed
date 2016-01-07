import webapp2
import json
import logging
from datetime import datetime
from handlers.mail import send_email
from google.appengine.api import blobstore
from service._users.sessions import BaseHandler
from db.database import Events, EventMatches, EventStandings,Departments
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from operator import itemgetter
from service._users.authentication import get_password_hash, passwords_match

class EventTime(webapp2.RequestHandler):

	def post(self):

		data=json.loads(self.request.body)
		event_code = int(data.get('event_id'))
		logging.info(event_code)
		time_string = data.get('time')
		location = data.get('location')
		match_type = data.get('match_type')
		dept1_code = data.get('dept1')
		dept2_code = data.get('dept2')
		result1=Departments.query(Departments.code_name==dept1_code).fetch()
		result2=Departments.query(Departments.code_name==dept2_code).fetch()
		result3=Events.query(Events.code==event_code).fetch()
		if len(result1) == 1 and len(result2) == 1 and len(result3) == 1:
			dept1_ptr = result1[0].key
			dept2_ptr = result2[0].key
			event_ptr = result3[0].key
			time = string_to_date(time_string)
			eve=EventMatches()
			eve.event_ptr = event_ptr
			eve.dept1_ptr = dept1_ptr
			eve.dept2_ptr = dept2_ptr
			eve.match_time = time
			eve.match_type = match_type
			eve.put()
			self.response.set_status(200,"Awesome")
			dict_ = {}
			dict_['status'] = "SUCCESS"
		else:
			self.response.set_status(400,"Failed")
			dict_ = {}
			dict_['status'] = "FAILED"

		self.response.write(json.dumps(dict_))



			