import webapp2
import logging
from datetime import datetime
from service._users.sessions import BaseHandler
from db.database import Channel_Admins, Users
from google.appengine.ext import ndb

class ChannelAdmins(BaseHandler, webapp2.RequestHandler):
	"""docstring for ChannelAdmins"""
	
	# Request URL: /channels/channel_id/admins POST
	# request params: array (user_id)
	# Response: status=200 else 400(not promoted)

	def post(self,channel_id):

		user_ids = self.request.get('user_id') #array of user_ids
		
		channel = Channels.get_by_id(int(channel_id))

		if channel:
			for user_id in user_ids:
				result = Users.query(Users.user_id == user_id).fetch()
				if len(result) == 1 :
					user = result[0]
					db = Channel_Admins()
					db.user_ptr = user.key
					db.channel_ptr = channel.key
					db.put()
					self.response.set_status(200,'Awesome')
					self.session['last-seen'] = datetime.now()
				else:
					self.response.set_status(401,'Unable to fetch user from Users.')
		else:
			self.response.set_status(400,'Unable to fetch channel from Channels.')	


	def delete(self,channel_id):
	# Request URL: /channels/:channel_id/admins DELETE
	# Response : status
		userID = self.session['userid']
		user_ptr = ndb.Key('Users',userID)		
		
		channel_ptr = ndb.Key('Channels', int(channel_id))
		logging.info(user_ptr)
		logging.info(channel_ptr)
		if channel_ptr and user_ptr:
			qury = Channel_Admins.query(Channel_Admins.user_ptr == user_ptr, Channel_Admins.channel_ptr == channel_ptr).fetch()
			if len(qury) == 1:
				channel_admin = qury[0]
				key = channel_admin.key
				if key:
					key.delete()
					self.response.set_status(200,'Awesome.You are no more admin.')
					self.session['last-seen'] = datetime.now()
				else:
					self.response.set_status(400,'Unable to fetch key.')	
			else:
				self.response.set_status(401,'Duplicate channel-admin combo!!!')
		else:
			self.response.set_status(401,'Channel Admin cannot be deleted.')