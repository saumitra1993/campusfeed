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
	img = ndb.BlobProperty()
	last_seen = ndb.DateTimeProperty(auto_now_add = True)  #update after discover channel API call

class Channels(ndb.Model):
	"""docstring for Channel"""
	
	#channel_id = [p]	
	channel_name = ndb.StringProperty()
	img = ndb.BlobProperty()
	description = ndb.StringProperty()
	pending_bit = ndb.IntegerProperty(default=1)	#keep it 1 while inserting
	curated_bit = ndb.IntegerProperty(default=1)	#curated/open, 1 means curated(rok k rakho salle ko!)
	isDeleted = ndb.IntegerProperty(default=0)
	edited_time = ndb.DateTimeProperty(auto_now = True)
	created_time = ndb.DateTimeProperty(auto_now_add = True)
	tag = ndb.StringProperty(
		choices = ['club','event','course','committee'])
	# DOCUMENT ADDED TO BE SEARCHED AFTER APPROVAL IN CHANNEL HANDLER PUT API
	# def _post_put_hook(self, future):
	# 	if self == future.get_result().get():
	# 		name = self.channel_name
	# 		descr = self.description
	# 		channel_id = str(self.key.id())
	# 		fields = [
	# 		  search.TextField(name="channel_name", value=name),
	# 		  search.TextField(name="channel_descr", value=descr),]
	# 		d = search.Document(doc_id=channel_id, fields=fields)
	# 		try:
	# 			add_result = search.Index(name="channelsearch").put(d)
	# 		except search.Error:	  
	# 			logging.error("Document not saved in index!")

class Posts(ndb.Model):
	"""docstring for Post"""

	#post_id = [p]
	user_ptr = ndb.KeyProperty(kind=Users)
	channel_ptr = ndb.KeyProperty(kind=Channels)
	text = ndb.TextProperty()
	img = ndb.BlobProperty(default='')
	created_time = ndb.DateTimeProperty(auto_now_add = True)
	pending_bit = ndb.IntegerProperty(default=1)
	isAnonymous = ndb.StringProperty(
					choices = ['True','False'],
					default = 'False')	#True means anonymous
	edited_time = ndb.DateTimeProperty(auto_now = True)
	post_by = ndb.StringProperty(
					choices = ['user','channel'],
					default = 'user')	
	isDeleted = ndb.IntegerProperty(default=0)

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
	getNotification = ndb.IntegerProperty(
					choices = [0,1],
					default = 0)
	last_seen = ndb.DateTimeProperty()

class DBMobileAuth(ndb.Model):
	name = ndb.StringProperty(indexed=False)
	user_id = ndb.StringProperty(indexed=True)
	expiration = ndb.DateTimeProperty(auto_now_add=True)
	@property
	def token(self):
		return self.key.id()

class Views(ndb.Model):
	"""docstring for Upvote"""
	user_ptr = ndb.KeyProperty(kind=Users)
	post_ptr = ndb.KeyProperty(kind=Posts)
	created_time = ndb.DateTimeProperty(auto_now_add=True)

	

# class Upvote_Notifications(ndb.Model):
# 	user_ptr = ndb.KeyProperty(kind=Users)
# 	post_ptr = ndb.KeyProperty(kind=Posts)
# 	new_upvote_count = ndb.IntegerProperty(default=0)

class DBUserGCMId(ndb.Model):
    """ Database to store the GCM Id when a user logs in
        GCM id is used to send push message
    """
    user_ptr = ndb.KeyProperty(kind=Users)
    gcm_id = ndb.StringProperty(indexed=False)
    creation_time = ndb.DateTimeProperty(auto_now_add=True)

class DBUserForgotPassword(ndb.Model):

	user_ptr = ndb.KeyProperty(kind=Users)
	fid = ndb.StringProperty(indexed=True)
	creation_time = ndb.DateTimeProperty(auto_now_add=True)

class DBUserChannelId(ndb.Model):

	user_ptr = ndb.KeyProperty(kind=Users)
	channel_id = ndb.StringProperty(indexed=True)
	tries = ndb.IntegerProperty(default=0)

class Threads(ndb.Model):

	channel_ptr = ndb.KeyProperty(kind=Channels)
	started_by_user_ptr = ndb.KeyProperty(kind=Users)
	created_time = ndb.DateTimeProperty(auto_now_add=True)
	topic = ndb.StringProperty(indexed=True)
	isDeleted = ndb.IntegerProperty(default=0)

class ThreadDiscussions(ndb.Model):

	thread_ptr = ndb.KeyProperty(kind=Threads)
	user_ptr = ndb.KeyProperty(kind=Users)
	text = ndb.TextProperty()
	added_time = ndb.DateTimeProperty(auto_now_add=True)
	isDeleted = ndb.IntegerProperty(default=0)

class ThreadViews(ndb.Model):

	thread_ptr = ndb.KeyProperty(kind=Threads)
	user_ptr = ndb.KeyProperty(kind=Users)
	created_time = ndb.DateTimeProperty(auto_now_add=True)

class PostFiles(ndb.Model):
	post_ptr = ndb.KeyProperty(kind=Posts)
	file_key = ndb.BlobKeyProperty()