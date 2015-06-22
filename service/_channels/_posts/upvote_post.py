import webapp2
import logging
from google.appengine.ext import ndb
from db.database import Upvotes,Posts
from service._users.sessions import BaseHandler

class UpvotePost(webapp2.RequestHandler,Basehandler):
	"""docstring for UpvotePost"""
	
	# DBtable : user_id,post_id,timestamp
	# Request URL: /posts/:post_id/upvotes POST
	# Response: status:200/400


	def post(self,post_id):

		user_ID = self.session['userid']
		user_ID = ndb.Key('Users',user_ID)

		query = Upvotes.query(Upvotes.user_ptr == user_ID, Upvotes.post_ptr == post_id)
		result = query.fetch()
		
		if len(result) == 1:
			self.response.set_status(401, 'User has already upvoted. Ask him to go fuck himself.')
		else:
			db1 = Posts.get_by_id(int(post_id))
			if db1: 
				db = Upvotes()
				db.user_ptr = user_ID
				db.post_ptr = db1.key
				db.put()
				self.response.set_status(200,'Awesome')
			else:
				self.response.set_status(400,'Unable to fetch post from Posts.')

