import webapp2
import logging
import json
from datetime import datetime, timedelta
from db.database import Channels, Users, Channel_Admins, Channel_Followers
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from service._users.sessions import BaseHandler, LoginRequired
from google.appengine.ext import ndb
from google.appengine.api import search

class ChannelsHandler(BaseHandler, webapp2.RequestHandler):
		
	# 	Request URL: /channels/:channel_id GET
	# Response : status, description, created_time, admins: array of (full_name)

	def get(self, channel_id):
		channel = Channels.get_by_id(int(channel_id))
		dict_ = {}
		if channel:
			channel_admins = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).fetch()
			if len(channel_admins) > 0:
				dict_['description'] = channel.description
				dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
				dict_['channel_name'] = channel.channel_name
				dict_['created_time'] = date_to_string(utc_to_ist(channel.created_time))
				
				
				dict_['pending_bit'] = 0
				if channel.img != '':
					dict_['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())+"?full=true"
				else:
					dict_['channel_img_url'] = DEFAULT_IMG_URL+"?full=true"
				out = []
				for channel_admin in channel_admins:
					_dict = {}
					if channel_admin.isAnonymous == 'True': #for admins who don't want to reveal their names.
						_dict['full_name'] = 'Anonymous'
					else:
						admin = channel_admin.user_ptr.get()
						_dict['full_name'] = admin.first_name + ' ' + admin.last_name
					
					out.append(_dict)
				dict_['admins'] = out
			else:
				self.response.set_status(400, 'No admins of the channel! Weird!')
				return
			try:
				user_id = int(self.userid)
				user = Users.get_by_id(user_id)
			
				if user:
					dict_['is_admin'] = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).count()
					dict_['is_following'] = Channel_Followers.query(Channel_Followers.user_ptr == user.key, Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
					self.response.set_status(200, 'Awesome')
				else:
					self.response.set_status(400, 'No admins of the channel! Weird!')
					return
			except:

				dict_['is_admin'] = 0
				dict_['is_following'] = 0
				self.response.set_status(200, 'Awesome')
				
		else:
			self.response.set_status(404, 'Channel not found')

		self.response.write(json.dumps(dict_))

	@LoginRequired
	def put(self, channel_id):

		userID = int(self.userid)
		user = Users.get_by_id(userID)
		logging.info("Hello!")
		if user.type_ == 'superuser':
			if channel_id:	
				db = Channels.get_by_id(int(channel_id))

				#approving a Channel by the superuser
				logging.info(db.pending_bit)
				if db.pending_bit == 1:
					db.pending_bit = 0
				logging.info(db.pending_bit)
				db.put()
				
				#inserting every ADMIN as FOLLOWER of his/her CHANNEL in Channel_Followers
				result = Channel_Admins.query(Channel_Admins.channel_ptr == db.key) #every admin is follower of HIS channel
				channel_admins_details = result.fetch()
				if len(channel_admins_details)>0 :
					for channel_admin_details in channel_admins_details:
						db1 = Channel_Followers()
						db1.user_ptr = channel_admin_details.user_ptr
						db1.channel_ptr = channel_admin_details.channel_ptr
						db1.put() 
				else:
					logging.info('Admin/s could NOT be inserted as Follower/s of their Channel.')
				
				name = db.channel_name
				descr = db.description
				channel_id = str(db.key.id())
				fields = [
				search.TextField(name="channel_name", value=name),
				search.TextField(name="channel_descr", value=descr),]
				d = search.Document(doc_id=channel_id, fields=fields)
				try:
					add_result = search.Index(name="channelsearch").put(d)
				except search.Error:	  
					logging.error("Document not saved in index!")

				self.response.set_status(200, 'Awesome.Channel approved by SUPERUSER.Admins becomes Followers of their Channel.')
		else:
			self.response.set_status(400, 'You are not an SUPERUSER.You cannot approve a CHANNEL.')

			