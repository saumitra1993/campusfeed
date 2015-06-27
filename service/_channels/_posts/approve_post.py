import webapp2
import logging
from db.database import Posts, Channel_Admins, Channels
from service._users.sessions import BaseHandler

class OnePost(BaseHandler, webapp2.RequestHandler):
	"""docstring for ApprovePost"""
	
	# Request URL : channels/:channel_id/posts/:post_id PUT
	# Response: status=200 else 400

	def put(self, channel_id, post_id):

		user_id = self.session['userid']
		user = Users.get_by_id(user_id)
		channel_key = Key('Channel', int(channel_id))
		if user.type_ == 'admin':
			users_channel = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel_key).fetch()
			if len(users_channel) == 1:
				db = Posts.get_by_id(int(post_id))
				logging.info(db.pending_bit)
				if db.pending_bit == 1:
					db.pending_bit = 0
				logging.info(db.pending_bit)
				db.put()
				self.response.set_status(200, 'Awesome.Post approved')
			else:
				self.response.set_status(400, 'You are not an ADMIN of this channel.You cannot approve a POST.')
		else:
			self.response.set_status(400, 'You are not an ADMIN.You cannot approve a POST.')

	
	# RequestURL: /channels/:channel_id/posts/:post_id GET
	# Response: text,post_img_url,description

	def get(self,channel_id,post_id):

		channel = Channels.get_by_id(int(channel_id))
		
		if channel:
			result = Posts.query(Posts.channel_ptr == channel.key).fetch()
			if len(result) == 1 :
				post = result[0]
				dict_ = {	
							'post_id' : post.key.id(),
				            'post_text' : post.text,
				            'post_description' : post.description,
				            'post_img_url' : post.post_img_url,
				        }
				logging.info(json.dumps(dict_, indent=2))
		        
		        response = json.dumps(dict_)
		        self.response.write(response)
		    else:
		    	self.response.set_status(401,'Unable to fetch post from Posts.')
		else:
			self.response.set_status(400,'Unable to fetch channel from Channels.')    