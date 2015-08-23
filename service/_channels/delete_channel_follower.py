import webapp2
import logging
import json
from operator import itemgetter
from datetime import datetime, timedelta
from google.appengine.ext import ndb
from service._users.sessions import BaseHandler, LoginRequired
from db.database import Channels, Users, Channel_Followers, Channel_Admins, Posts
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_ROOT_URL, DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, tags

class DeleteChannelFollower(BaseHandler, webapp2.RequestHandler):
	


	#delete user_id and channel_id from Channel_Followers
	def post(self, user_id):
		data = json.loads(self.request.body)
		channel_id = int(data.get('channel_id').strip())
		channel_ptr = ndb.Key('Channels', channel_id)
		user_id = int(user_id)
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			query = Channel_Followers.query(Channel_Followers.user_ptr == user_ptr, Channel_Followers.channel_ptr == channel_ptr).fetch()
			if len(query) == 1:
				user_channel = query[0]
				logging.info(user_channel)
				key = user_channel.key
				if key:
				#   key.delete()    
					db = Channel_Followers.get_by_id(int(key.id()))
					if db.isDeleted == 0:
						db.isDeleted = 1
						db.put()
						self.response.set_status(200,'Awesome.Entry deleted.')
				else:
					self.response.set_status(400,'Unable to fetch key.')
			else:
				self.response.set_status(401,'Duplicate or none user_ptr-channel_ptr combo!!!')
		else:
			self.response.set_status(401,'Channel Follower cannot be deleted as User can\'t be fetched.')
