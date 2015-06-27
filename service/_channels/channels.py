import webapp2
import json
import logging
from datetime import datetime
from google.appengine.api import blobstore
from service._users.sessions import BaseHandler
from db.database import Users, Channel_Admins, Channels, Channel_Followers
from google.appengine.ext.webapp import blobstore_handlers
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID

class AllChannels(blobstore_handlers.BlobstoreUploadHandler, BaseHandler):
	"""docstring for Channels"""
	# Request URL - /channels POST
	# Request params - user_id, channel_name, channel_img_url, description, curated_bit, isAnonymous
	# Response - status

	def post(self):

		logging.info(self.request)

		user_id = self.request.get('user_id').strip()
		isAnonymous = self.request.get('isAnonymous').strip()
		user_query = Users.query(Users.user_id == user_id).fetch() #query will store entire 'list' of db cols
		if len(user_query) == 1:
			user = user_query[0]
			user_key = user.key
			user.type_ = 'admin'   #updating 'user' to 'admin
			user.put()
			db = Channels()
			db.channel_name = self.request.get('channel_name').strip()
			db.description = self.request.get('description').strip()
			db.curated_bit = int(self.request.get('curated_bit').strip())
			db.channel_img_url = self.get_uploads('channel_img_url')[0].key()
			logging.info(db.channel_img_url)
			k = db.put()
			channel_items = k.get()
			channel_key = channel_items.key

			

			db1 = Channel_Admins()
			db1.user_ptr = user_key
			db1.channel_ptr = channel_key
			db1.isAnonymous = isAnonymous
			k1 = db1.put()
			self.session['last-seen'] = datetime.now()
			db2 = Channel_Followers()
			db2.user_ptr = user_key
			db2.channel_ptr = channel_key
			k2 = db2.put()
			logging.info('...Inserted into DB user with key... %s ' % k1)

	# Request URL - /channels GET

	# Response - Dictionary of status, all_channels: array of (channel_id, channel_name, channel_img_url, num_folllowers)

	# Query params-
	# limit and offset
	def get(self):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		timestamp = self.request.get('timestamp')
		_dict = {}
		if limit and offset:
			limit = int(limit)
			offset= int(offset)
			user_id = self.session['userid']
			user = Users.get_by_id(user_id)
			channels_qry = Channel_Followers.query(Channel_Followers.user_ptr != user.key)
			if timestamp:
				lastSeenTime = string_to_date(timestamp) 
				lastSeenTime = ist_to_utc(lastSeenTime)
				channels_qry = channels_qry.filter(Channel_Followers.created_time >= lastSeenTime)
			if limit!=-1:
				channel_keys = channels_qry.fetch(limit,offset= offset)
			else:
				channel_keys = channels_qry.fetch(offset= offset)

			out = []
			for channel_key in channel_keys:
				channel = Channels.get_by_id(channel_key.id())
				dict_ = {}
				dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key).count()
				dict_['channel_id'] = channel.key.id()
				dict_['channel_name'] = channel.channel_name
				if channel.channel_img_url:
					dict_['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.channel_img_url)
				else:
					dict_['channel_img_url'] = DEFAULT_IMG_URL

				if len(out) > 0:
					i = 0
					for elem in out:
						i = i+1
						if elem['num_followers'] < dict_['num_followers']:
							out[:i-1].append(dict_) + out[i:]
						elif i == len(out):
							out.append(dict_)
				else:
					out.append(dict_)

			_dict['all_channels'] = out
			self.response.set_status(200, 'Awesome')
			self.session['last-seen'] = datetime.now()
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(_dict))