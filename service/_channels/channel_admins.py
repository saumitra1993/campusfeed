import webapp2
import logging
from service._users.sessions import BaseHandler
from db.database import Channel_Admins, Users

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
				else:
					self.response.set_status(401,'Unable to fetch user from Users.')
		else:
			self.response.set_status(400,'Unable to fetch channel from Channels.')			
