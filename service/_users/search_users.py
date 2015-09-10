import webapp2
import logging
import json
from db.database import Users
from google.appengine.ext import ndb
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID


class SearchUsers(webapp2.RequestHandler):
	"""docstring for SearchUser"""
	
	# Request URL: /users/search?search_string=search_query GET
	# Response: results: dict(array of(first_name,last_name,user_id,user_img_url,branch))
	# DATA IN DATABASE IS ALWAYS COMPLETELY title case
	def get(self):

		first_name = self.request.get('first_name').strip() #search_string is a name(first/last)
		last_name = self.request.get('last_name').strip()
		matching_users = Users.query(ndb.OR(Users.first_name == first_name, Users.last_name == last_name)).fetch()
		dict_ = {}
		out = []
		for matching_user in matching_users:
			_dict = {}
			_dict['user_id'] = matching_user.user_id
			_dict['name'] = matching_user.first_name + " " + matching_user.last_name
			if matching_user.img!='':
				_dict['user_img_url'] = DEFAULT_ROOT_IMG_URL + str(matching_user.key.urlsafe())
			else:
				_dict['user_img_url'] = DEFAULT_IMG_URL
			out.append(_dict)
		dict_['results'] = out
		self.response.set_status(200,'Awesome')
		self.response.write(json.dumps(dict_))

