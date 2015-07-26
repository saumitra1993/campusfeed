import webapp2
import logging
from datetime import datetime
from db.database import Posts, Channel_Admins, Channels, Views, Users
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb

class OnePost(BaseHandler, webapp2.RequestHandler):
	"""docstring for ApprovePost"""
	
	# Request URL : channels/:channel_id/posts/:post_id PUT
	# Response: status=200 else 400

	def put(self, channel_id, post_id):

		user_id = self.session['userid']
		user = Users.get_by_id(user_id)
		channel_key = ndb.Key('Channels', int(channel_id))
		if user.type_ == 'admin' or user.type_ == 'superuser':
			users_channel = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel_key, Channel_Admins.isDeleted == 0).fetch()
			if len(users_channel) == 1:
				db = Posts.get_by_id(int(post_id))
				if db.pending_bit == 1:
					db.pending_bit = 0
				logging.info(db.pending_bit)
				db.put()
				self.session['last-seen'] = datetime.now()
				self.response.set_status(200, 'Awesome.Post approved')
			else:
				self.response.set_status(400, 'You are not an ADMIN of this channel.You cannot approve a POST.')
		else:
			self.response.set_status(400, 'You are not an ADMIN.You cannot approve a POST.')

	
	# RequestURL: /channels/:channel_id/posts/:post_id GET
	# Response: text,post_img_url,description

	def get(self,channel_id,post_id):
		logged_in_userid = self.session['userid']
		logged_in_user_key = Key('Users',logged_in_userid)
		post = Posts.get_by_id(int(post_id))
		if post:
			user = post.user_ptr.get()
			channel = post.channel_ptr.get()
			if post.isAnonymous == 'True':
				name = 'Anonymous'
			else:
				if post.post_by == 'user':
					name = user.first_name + ' ' + user.last_name
				else:
					_dict['full_name'] = channel.channel_name
			
			num_views = Views.query(Views.post_ptr == post.key).count()
			dict_ = {	
						'post_id' : post.key.id(),
						'post_text' : post.text,
						'created_time':date_to_string(utc_to_ist(post.created_time)),
						'channel_id':channel.key.id(),
						'channel_name':channel.channel_name,
						'user_id':user.key.id(),
						'user_name': name,
						'num_Views':num_views,
					}
			if post.img != '':
				dict_['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(post.key.urlsafe())
			else:
				dict_['post_img_url'] = ''
			dict_['post_by'] = post.post_by
			logging.info(json.dumps(dict_, indent=2))
			# notifications_query = Upvote_Notifications.query(Upvote_Notifications.user_ptr == logged_in_user_key, Upvote_Notifications.post_ptr == post.key).fetch()
			# if len(notifications_query) == 1:
			# 	new_notif = notifications_query[0]
			# 	new_notif.new_upvote_count = 0
			# 	new_notif.put()
			response = json.dumps(dict_)
			self.session['last-seen'] = datetime.now()
			self.response.set_status(200, 'Awesome')
			self.response.write(response)
		else:
			self.response.set_status(400,'Unable to fetch channel from Channels.')    