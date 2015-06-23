import webapp2
import logging

class SearchUsers(webapp2.RequestHandler):
	"""docstring for SearchUser"""
	
	# Request URL: /users/search?search_string=search_query GET
	# Response: results: dict(array of(first_name,last_name,user_id,user_img_url,branch))

	def get(self):

		search_string = self.request.get('search_string').strip() #search_string is a name(first/last)

		db = 

