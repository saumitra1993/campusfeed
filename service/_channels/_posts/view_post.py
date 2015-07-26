import webapp2
import logging
from google.appengine.ext import ndb
from db.database import Views,Posts
from service._users.sessions import BaseHandler

class PostViewed(BaseHandler, webapp2.RequestHandler):
	"""docstring for UpvotePost"""
	
	# DBtable : user_id,post_id,timestamp
	# Request URL: /posts/:post_id/views POST
	# Response: status:200/400


	def post(self,post_id):

		user_ID = self.session['userid']
		user_ID = ndb.Key('Users',user_ID)
		post_key = ndb.Key('Posts',post_id)
		query = Views.query(Views.user_ptr == user_ID, Views.post_ptr == post_key)
		result = query.fetch()
		
		if len(result) == 1:
			self.response.set_status(401, 'User has already upvoted. Ask him to go fuck himself.')
		else:
			db1 = Posts.get_by_id(int(post_id))
			if db1: 
				db = Views()
				db.user_ptr = user_ID
				db.post_ptr = db1.key
				db.put()
				# notifications_query = Upvote_Notifications.query(Upvote_Notifications.user_ptr == user_ID, Upvote_Notifications.post_ptr == db1.key).fetch()
				# if len(notifications_query) == 1:
				# 	new_notif = notifications_query[0]
				# 	new_notif.new_upvote_count = new_notif.new_upvote_count + 1
				# 	new_notif.put()
				# else:
				# 	new_notif = Upvote_Notifications()
				# 	new_notif.user_ptr = user_ID
				# 	new_notif.post_ptr = db1.key
				# 	new_notif.new_upvote_count = 1
				# 	new_notif.put()
				self.response.set_status(200,'Awesome')
			else:
				self.response.set_status(400,'Unable to fetch post from Posts.')

