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
	curated_bit = ndb.IntegerProperty(default=1)	#curated/open, 1 means curated(rok k rakho salle ko!)
	created_time = ndb.DateTimeProperty(auto_now_add = True)



class Posts(ndb.Model):
	"""docstring for Post"""

	#post_id = [p]
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	text = ndb.StringProperty()
	post_img_url = ndb.BlobKeyProperty()
	time = ndb.DateTimeProperty(auto_now_add = True)
	pending_bit = ndb.IntegerProperty(default=1)
	isAnonymous = ndb.StringProperty(
					choices = ['True','False'],
					default = 'True')	#True means pending

class Channel_Admins(ndb.Model):
	"""docstring for Channel_Admin"""
	
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	isAnonymous = ndb.StringProperty(
					choices = ['True','False'],
					default = 'True')

class Channel_Followers(ndb.Model):
	"""docstring for Channel_Followers"""

	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)

class DBMobileAuth(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    user_id = ndb.StringProperty(indexed=True)
    expiration = ndb.DateTimeProperty(auto_now_add=True)
    @property
    def token(self):
        return self.key.id()