import webapp2
import logging
import json
from db.database import Channels, Users, Channel_Admins, Channel_Followers
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb

class Notifications(BaseHandler, webapp2.RequestHandler):

	# Request URL: users/:userid/notifications GET
	# Response:
	#  dict: {
	#     'admin_notif': channel_id, channel_name, user_id, user_first_name,lastname,bit  #admin added/removed
	#     'channel_notif': 
	#     'post_notif':
	#     'upvote_notif':
	#     'follow_notif':
	#  }
	def get(self, user_id):
		user_query = Users.query(Users.user_id == user_id)
		result = user_query.fetch()
		final_dict = {}
		if len(result) == 1:
			user = result[0]
			lastSeen = self.session['last-seen']
			if user.type_ == 'admin':
				admins_query = Channel_Admins.query(Channel_Admins.user_ptr == user.key)
				admin_to_new_channels = admins_query.filter(Channel_Admins.created_time > lastSeen).fetch()
				out1 = []
				for admin_to_new_channel in admin_to_new_channels:
					channel_ptr = admin_to_new_channel.channel_ptr
					channel = channel_ptr.get()
					dict_ = {}
					dict_['channel_id'] = channel.key.id()
					dict_['channel_name'] = channel.channel_name
					out1.append(dict_)

				final_dict['new_as_admin'] = out1
				admin_to_channels = admins_query.fetch()
				out2 = []
				out3 = []
				for admin_channel in admin_to_channels:
					dict_ = {}
					dict_2 = {}
					channel = admin_channel.channel_ptr.get()
					new_posts = Posts.query(Posts.channel_ptr == channel.key, Posts.created_time > lastSeen).count()
					if new_posts > 0:
						dict_['channel_id'] = channel.key.id()
						dict_['channel_name'] = channel.channel_name
						dict_['num_new_posts'] = new_posts
						out2.append(dict_)

					new_followers_count = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.created_time > lastSeen).count()
					if new_followers_count > 0:
						dict_2['channel_id'] = channel.key.id()
						dict_2['channel_name'] = channel.channel_name
						dict_2['num_new_followers'] = new_followers_count
						out3.append(dict_2)
				final_dict['new_posts'] = out2
				final_dict['new_followers'] = out3

