import webapp2
import logging
import json
from datetime import datetime
from service._users.sessions import BaseHandler, LoginRequired
from db.database import *
from google.appengine.ext import ndb

class ChannelAdmins(BaseHandler, webapp2.RequestHandler):
	"""docstring for ChannelAdmins"""
	
	# Request URL: /channels/channel_id/admins POST
	# request params:  (user_id, isAnonymous)
	# Response: status=200 else 400(not promoted)
	@LoginRequired
	def post(self,channel_id):
		data = json.loads(self.request.body)
		user_id = data.get('user_id')	 
		isAnonymous = data.get('isAnonymous')
		channel = Channels.get_by_id(int(channel_id))
		logged_in_userid = int(self.userid)
		logged_in_user = Users.get_by_id(logged_in_userid)
		if channel:
			check_if_admin_query = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key, Channel_Admins.user_ptr == logged_in_user.key).fetch()
			if len(check_if_admin_query) == 1:
				result = Users.query(Users.user_id == user_id).fetch()
				if len(result) == 1 :
					user = result[0]
					if_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key, Channel_Admins.user_ptr == user.key).count()
					if if_admin == 0:
						user.type_ ='admin'
						user.put()
						db = Channel_Admins()
						db.user_ptr = user.key
						db.channel_ptr = channel.key
						if isAnonymous:
							db.isAnonymous = 'True' #for user who don't want to reveal his name as admin						
						db.put()
						db1 = Channel_Followers()
						db1.user_ptr = user.key
						db1.channel_ptr = channel.key
						db1.put()
					self.response.set_status(200,'Awesome')
				else:
					self.response.set_status(401,'Unable to fetch user from Users.')
			else:
				self.response.set_status(401,'Unauthorized')
		else:
			self.response.set_status(400,'Unable to fetch channel from Channels.')	

	@LoginRequired
	def delete(self,channel_id):
	# Request URL: /channels/:channel_id/admins DELETE
	# Response : status
		userID = int(self.userid)
		user_ptr = ndb.Key('Users',userID)		
		
		channel_ptr = ndb.Key('Channels', int(channel_id))
	
		if channel_ptr and user_ptr:
			query = Channel_Admins.query(Channel_Admins.user_ptr == user_ptr, Channel_Admins.channel_ptr == channel_ptr).fetch()
			if len(query) == 1:
				channel_admin = query[0]
				key = channel_admin.key
				if key:
			#		key.delete()
					db = Channel_Admins.get_by_id(int(key.id()))
					if db.isDeleted == 0:
						db.isDeleted = 1
						db.put()
						self.response.set_status(200,'Awesome.You are no more admin.')
					else:
						self.response.set_status(400,'Sorry,you are already NOT an admin.')	
			else:
				self.response.set_status(401,'Duplicate channel-admin combo!!!')
		else:
			self.response.set_status(401,'Channel Admin cannot be deleted.')