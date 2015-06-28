import webapp2
import logging
import json
from db.database import Users
from google.appengine.ext import ndb


class SearchUsers(webapp2.RequestHandler):
	"""docstring for SearchUser"""
	
	# Request URL: /users/search?search_string=search_query GET
	# Response: results: dict(array of(first_name,last_name,user_id,user_img_url,branch))
	# DATA IN DATABASE IS ALWAYS COMPLETELY LOWERCASE
	def get(self):

		search_string = self.request.get('search_string').strip() #search_string is a name(first/last)
		matching_users = Users.query(ndb.OR(Users.first_name == search_string, Users.last_name == search_string)).fetch()
		dict_ = {}
		out = []
		for matching_user in matching_users:
			_dict = {}
			_dict['user_id'] = matching_user.user_id
			_dict['name'] = matching_user.first_name + " " + matching_user.last_name
			out.append(_dict)
		dict_['results'] = out
		self.response.set_status(200,'Awesome')
		self.response.write(json.dumps(dict_))

