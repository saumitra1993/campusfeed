import webapp2
import logging
from db.database import Posts
from service._users.sessions import BaseHandler

class OnePost(webapp2.RequestHandler, BaseHandler):
	"""docstring for ApprovePost"""
	
	# Request URL : channels/:channel_id/posts/:post_id PUT
	# Response: status=200 else 400

	def put(self, channel_id, post_id):

		user_id = self.session['userid']
		user = Users.get_by_id(user_id)
		
		if user.type_ == 'admin':
			db = Posts.get_by_id(int(post_id))
			logging.info(db.pending_bit)
			if db.pending_bit == 1:
				db.pending_bit = 0
			logging.info(db.pending_bit)
			db.put()
			self.response.set_status(200, 'Awesome.Post approved')
		else:
			self.response.set_status(400, 'You are not an ADMIN.You cannot approve a POST.')