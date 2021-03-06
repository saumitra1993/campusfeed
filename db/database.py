from google.appengine.ext import ndb
from google.appengine.api import search
import logging

index1 = search.Index(name='channelsearch')

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
	user_img_url = ndb.BlobKeyProperty()
	last_seen = ndb.DateTimeProperty() # given when the app gets killed/update after every api call

class Channels(ndb.Model):
	"""docstring for Channel"""
	
	#channel_id = [p]	
	channel_name = ndb.StringProperty()
	channel_img_url = ndb.BlobKeyProperty()
	description = ndb.StringProperty()
	pending_bit = ndb.IntegerProperty(default=1)	#keep it 1 while inserting
	curated_bit = ndb.IntegerProperty(default=1)	#curated/open, 1 means curated(rok k rakho salle ko!)
	isDeleted = ndb.IntegerProperty(default=0)
	edited_time = ndb.DateTimeProperty(auto_now = True)
	created_time = ndb.DateTimeProperty(auto_now_add = True)

	def _post_put_hook(self, future):
		if self == future.get_result().get():
			name = self.channel_name
			descr = self.description
			channel_id = str(self.key.id())
			fields = [
			  search.TextField(name="channel_name", value=name),
			  search.TextField(name="channel_descr", value=descr),]
			d = search.Document(doc_id=channel_id, fields=fields)
			try:
				add_result = search.Index(name="channelsearch").put(d)
			except search.Error:	  
				logging.error("Document not saved in index!")

class Posts(ndb.Model):
	"""docstring for Post"""

	#post_id = [p]
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	text = ndb.StringProperty()
	post_img_url = ndb.BlobKeyProperty()
	created_time = ndb.DateTimeProperty(auto_now_add = True)
	pending_bit = ndb.IntegerProperty(default=1)
	isAnonymous = ndb.StringProperty(
					choices = ['True','False'],
					default = 'False')	#True means pending
	edited_time = ndb.DateTimeProperty(auto_now = True)
#	isDeleted = ndb.IntegerProperty(default=0)

class Channel_Admins(ndb.Model):
	"""docstring for Channel_Admin"""
	
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	isAnonymous = ndb.StringProperty(
					choices = ['True','False'],
					default = 'False')
	created_time = ndb.DateTimeProperty(auto_now_add = True)
	isDeleted = ndb.IntegerProperty(default=0)
	edited_time = ndb.DateTimeProperty(auto_now = True)

class Channel_Followers(ndb.Model):
	"""docstring for Channel_Followers"""

	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	created_time = ndb.DateTimeProperty(auto_now_add = True)
	edited_time = ndb.DateTimeProperty(auto_now = True)
	isDeleted = ndb.IntegerProperty(default=0)

class DBMobileAuth(ndb.Model):
	name = ndb.StringProperty(indexed=False)
	user_id = ndb.StringProperty(indexed=True)
	expiration = ndb.DateTimeProperty(auto_now_add=True)
	@property
	def token(self):
		return self.key.id()

class Upvotes(ndb.Model):
	"""docstring for Upvote"""
	user_ptr = ndb.KeyProperty(kind=Users)
	post_ptr = ndb.KeyProperty(kind=Posts)
	created_time = ndb.DateTimeProperty(auto_now_add=True)

	#self.session['userid'] ... this is badi wali id 
	#chinmay will always send me 14307(one in the url),since it has never been sent from backend

class Upvote_Notifications(ndb.Model):
	user_ptr = ndb.KeyProperty(kind=Users)
	post_ptr = ndb.KeyProperty(kind=Posts)
	new_upvote_count = ndb.IntegerProperty(default=0)