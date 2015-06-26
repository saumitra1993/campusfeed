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

		user_ids = self.request.get('user_id') #array of user_ids(sent by Chinmay)
		isAnonymous = self.request.get('is_Anonymous').strip()
		channel = Channels.get_by_id(int(channel_id))

		if channel:
			for user_id in user_ids:
				result = Users.query(Users.user_id == user_id).fetch()
				if len(result) == 1 :
					user = result[0]
					db = Channel_Admins()
					db.user_ptr = user.key
					db.channel_ptr = channel.key
					if isAnonymous:
						db.isAnonymous = 'True' #for user who don't want to reveal his name as admin						
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
	
		if channel_ptr and user_ptr:
			query = Channel_Admins.query(Channel_Admins.user_ptr == user_ptr, Channel_Admins.channel_ptr == channel_ptr).fetch()
			if len(query) == 1:
				channel_admin = query[0]
				key = channel_admin.key
			#	if key:
			#		key.delete()
				db = Channel_Admins.get_by_id(int(key.id()))
				if db.isDeleted == 0:
					db.isDeleted = 1
					db.put()
					self.session['last-seen'] = datetime.now()
					self.response.set_status(200,'Awesome.You are no more admin.')
				else:
					self.response.set_status(400,'Sorry,you are already NOT an admin.')	
			else:
				self.response.set_status(401,'Duplicate channel-admin combo!!!')
		else:
			self.response.set_status(401,'Channel Admin cannot be deleted.')