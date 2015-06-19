import webapp2
import logging
from db.database import Posts

class ApprovePost(webapp2.RequestHandler):
	"""docstring for ApprovePost"""
	
	# Request URL : channels/:channel_id/posts/:post_id PUT
	# Response: status=200 else 400

	def put(self, channel_id, post_id):

		db = Posts.get_by_id(int(post_id))
		logging.info(db.pending_bit)
		if db.pending_bit == 1:
			db.pending_bit = 0
		logging.info(db.pending_bit)
		db.put()