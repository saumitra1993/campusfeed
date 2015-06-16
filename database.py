from google.appengine.ext import ndb
import logging

class User(ndb.Model):
	"""docstring for User"""
	
	#user_id = [p]
	username = ndb.StringProperty()
	branch = ndb.StringProperty()
	type_ = ndb.StringProperty(
		choices = ['user','admin','superuser'],
		default = 'user')
	phone = ndb.StringProperty()
	email_id = ndb.StringProperty()
	password = ndb.StringProperty()
	user_id = ndb.StringProperty()
	instance_key = ndb.StringProperty()

class Channel(ndb.Model):
	"""docstring for Channel"""
	
	#channel_id = [p]	
	channel_name = ndb.StringProperty()
	channel_img_url = ndb.BlobKeyProperty()
	description = ndb.StringProperty()
	pending_bit = ndb.IntegerProperty()
	curated_bit = ndb.BooleanProperty()


class Post(ndb.Model):
	"""docstring for Post"""

	#post_id = [p]
	user_row = ndb.KeyProperty(kind=User)
	channel_row = ndb.KeyProperty(kind=Channel)
	text = ndb.StringProperty()
	img_url = ndb.BlobKeyProperty()
	time = ndb.DateTimeProperty(auto_now = True)
	pending_bit = ndb.IntegerProperty()
	isAnonymous = ndb.BooleanProperty()


class Channel_Admin(ndb.Model):
	"""docstring for Channel_Admin"""
	
	user_row = ndb.KeyProperty(kind=User)
	channel_row = ndb.KeyProperty(kind=Channel)
	isAnonymous = ndb.BooleanProperty()