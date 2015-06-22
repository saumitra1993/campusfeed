import webapp2
import logging

class ShowpendingPosts(webapp2.RequestHandler):
	"""docstring for ShowpendingPosts"""

# Request URL - /channels/:channel_id/pendingposts GET
# Response - Dictionary of status, posts: array of (  post_id(generated),
# 													text, img_url, time, 
# 													first_name, last_name, user_img_url, user_branch )