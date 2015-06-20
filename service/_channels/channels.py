import webapp2
import json
import logging
from db.database import Users, Channel_Admins, Channels
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class NewChannels(blobstore_handlers.BlobstoreUploadHandler):
	"""docstring for Channels"""
	# Request URL - /channels POST
	# Request params - user_id, channel_name, channel_img_url, description, curated_bit, isAnonymous
	# Response - status

	def post(self):

		logging.info(self.request)

		user_id = self.request.get('user_id').strip()
		isAnonymous = self.request.get('isAnonymous').strip()
		
		db = Channels()
		db.channel_name = self.request.get('channel_name').strip()
		db.description = self.request.get('description').strip()
		db.curated_bit = int(self.request.get('curated_bit').strip())
		db.channel_img_url = self.get_uploads('channel_img_url')[0].key()
		logging.info(db.channel_img_url)
		k = db.put()
		channel_items = k.get()
		channel_key = channel_items.key

		query = Users.query().filter(Users.user_id == user_id).fetch()
		user_key = query[0].key

		db1 = Channel_Admins()
		db1.user_ptr = user_key
		db1.channel_ptr = channel_key
		db1.isAnonymous = isAnonymous
		k1 = db1.put()
		logging.info('...Inserted into DB user with key... %s ' % k1)