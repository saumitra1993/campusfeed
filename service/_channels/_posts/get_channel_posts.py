import webapp2
import logging
import json
from db.database import Channels, Users, Posts
class GetChannelPosts(webapp2.RequestHandler):
	# 	Request URL: /channels/:channel_id/posts GET
	# Response: Dictionary of status, posts: array of (post_id(generated),text, img_url, time, user_full_name, user_img_url, user_branch )

	# Query params - limit, offset, timestamp
	def get(self, channel_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		timestamp = self.request.get('timestamp')
		dict_ = {}
		if limit and offset:
			limit = int(limit)
			offset= int(offset)
			channel = Channels.get_by_id(int(channel_id))
			if limit != -1:
				posts = Posts.query(Posts.channel_ptr == channel.key, Posts.pending_bit == 0).fetch(limit,offset=offset)
			else:
				posts = Posts.query(Posts.channel_ptr == channel.key, Posts.pending_bit == 0).fetch(offset=offset)
			out = []
			for post in posts:
				posting_user = Users.get_by_id(post.user_ptr.id())
				_dict = {}
				_dict['post_id'] = post.key.id()
				_dict['text'] = post.text
				_dict['img_url'] = post.img_url
				_dict['time'] = post.time
				_dict['user_full_name'] = posting_user.first_name+' '+posting_user.last_name
				_dict['user_img_url'] = posting_user.user_img_url
				_dict['branch'] = posting_user.branch
				out.append(_dict)
			dict_['posts'] = out
		elif limit and offset and timestamp:
			timestamp = time.strptime(timestamp,'%d %m %Y %H:%M:%S')