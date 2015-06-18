from google.appengine.ext import ndb
import logging

class Users(ndb.Model):
	"""docstring for User"""
	
	#user_id = [p]
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	branch = ndb.StringProperty()
	type_ = ndb.StringProperty(
		choices = ['user','admin','superuser'],
		default = 'user')
	phone = ndb.StringProperty()
	email_id = ndb.StringProperty()
	password = ndb.StringProperty()
	user_id = ndb.StringProperty()
	# instance_key = ndb.StringProperty()
	user_img_url = ndb.BlobKeyProperty()

class Channels(ndb.Model):
	"""docstring for Channel"""
	
	#channel_id = [p]	
	channel_name = ndb.StringProperty()
	channel_img_url = ndb.BlobKeyProperty()
	description = ndb.StringProperty()
	pending_bit = ndb.IntegerProperty()	#keep it 1 while inserting
	curated_bit = ndb.BooleanProperty()	#curated/open
	created_time = ndb.DateTimeProperty()



class Posts(ndb.Model):
	"""docstring for Post"""

	#post_id = [p]
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	text = ndb.StringProperty()
	img_url = ndb.BlobKeyProperty()
	time = ndb.DateTimeProperty(auto_now = True)
	pending_bit = ndb.IntegerProperty()
	isAnonymous = ndb.BooleanProperty()


class Channel_Admins(ndb.Model):
	"""docstring for Channel_Admin"""
	
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	isAnonymous = ndb.BooleanProperty()

class Channel_Followers(ndb.Model):
	"""docstring for Channel_Followers"""

	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
		