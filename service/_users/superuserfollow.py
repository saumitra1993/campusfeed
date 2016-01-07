import logging
import webapp2
import random
import string
import json
from datetime import datetime, timedelta
from db.database import *
from google.appengine.api import users
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class SuperuserFollow(BaseHandler, webapp2.RequestHandler):
	def get(self):


		f = open("static/points.txt")
		for line in f:
			lines = line.split('\r')
			for line in lines:
				arr = line.split(',')
				code = int(arr[0])
				name = arr[1].strip()
				type_of_event = arr[10].strip()
				event = Events()
				event.name = name
				event.code = code
				event.type_of_event = type_of_event
				event.p1 = int(arr[2])
				event.p2 = int(arr[3])
				event.p3 = int(arr[4])
				event.p4 = int(arr[5])
				event.p5 = int(arr[6])
				event.p6 = int(arr[7])
				event.p7 = int(arr[8])
				event.p8 = int(arr[9])
				event.put()
				
		f.close()

		depts = ['CSE','MME','CME','MIN','EEE','ECE','ARCHI']
		i = 0
		for dept in depts:
			d = Departments()
			d.code_name = depts[i]
			d.put()
			i = i + 1 
			
		self.response.set_status(200,"Awesome")
		self.response.write("dhg")

		# users = Users.query().fetch()
		# channel = Channels.get_by_id(5636432282517504)
		# channels_followers = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key).fetch()
		# for channel_follower in channels_followers:
		# 	key = channel_follower.key
		# 	key.delete()
		# for user in users:
		# 	db = Channel_Followers()
		# 	db.user_ptr = user.key
		# 	db.channel_ptr = channel.key
		# 	db.getNotification = 1
		# 	db.put()
		# channels_admins = Channel_Admins.query().fetch()
		# for chan_admin in channels_admins:
		# 	channel = chan_admin.channel_ptr.get()
		# 	if channel.tag != 'course' and channel.pending_bit == 0:
		# 		admin = chan_admin.user_ptr.get()
		# 		email_id = admin.email_id
		# 		first_name = admin.first_name
		# 		subject = "Making magic happen with your channel on Campusfeed!"
		# 		to = email_id
		# 		body = "Hi "+first_name+"! <br/>Now that you are up and running with a Campusfeed channel, here's a short how-to on how you can reimagine the way your club is run using Campusfeed. <br /> <br />1) Add all of your core members as admins of your channel so that all of them are able to post on the same. <br />2) Convert your current members/followers to followers on Campusfeed. <br /> 3) Engage your audience with posts starting from an introduction to your "+channel.tag+", past achievements, why is it important for people to follow you and your vision for the "+channel.tag+".<br />4) Use images to liven up your posts.<br/>5) <b>Your potential audience on Campusfeed is the entire college.</b><br /><br />  We hope Campusfeed helps you reach and lead your "+channel.tag+" like never before.<br /> <br /><b><i>We have worked hard to set up a stage for people who want to bring change. Over to you to leverage it. </i></b><br /><br /> Thanks,<br/>Campusfeed Team."
		# 		send_email(subject,to,body)


		
