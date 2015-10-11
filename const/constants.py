import os
import logging
test_server = os.environ.get('APPLICATION_ID', '') == 's~campusfeedapp'
prod_server = os.environ.get('APPLICATION_ID', '') == 's~campusfeed-1018'
dev_server = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
if dev_server:
	DEFAULT_ROOT_URL = 'http://localhost:9080/'
	DEFAULT_ROOT_IMG_URL = 'http://localhost:9080/pic/'
	DEFAULT_ROOT_FILE_URL = 'http://localhost:9080/files/'
	GCM_PUSH_MESSAGE_API_KEY = ''
elif prod_server:
	DEFAULT_ROOT_URL = 'http://campusfeedapp.com/'
	DEFAULT_ROOT_IMG_URL = 'http://campusfeedapp.com/pic/'
	DEFAULT_ROOT_FILE_URL = 'http://campusfeedapp.com/files/'
	GCM_PUSH_MESSAGE_API_KEY = "AIzaSyAuUTU-p8sM7SPpMNWYFig0lWcvyokyrRk"
elif test_server:
	DEFAULT_ROOT_URL = 'http://campusfeedapp.appspot.com/'
	DEFAULT_ROOT_IMG_URL = 'http://campusfeedapp.appspot.com/pic/'
	DEFAULT_ROOT_FILE_URL = 'http://campusfeedapp.appspot.com/files/'
	GCM_PUSH_MESSAGE_API_KEY = "AIzaSyCpt6EOj9TStOvDNbOeSqXCx125JEquvCc"

DEFAULT_IMG_URL = DEFAULT_ROOT_URL + 'images/default.png'
DEFAULT_ANON_IMG_URL = DEFAULT_ROOT_URL + 'images/anonymous.jpg'
MOBILE_USER_SESSION_DURATION_DAYS = 30
DEFAULT_IMG_ID = "lpwhf_cRJVOdru_4zmW3BA=="

GCM_PUSH_MESSAGE_API_KEY_MOBILE = GCM_PUSH_MESSAGE_API_KEY
tags = ['course', 'event', 'club', 'committee']
POST_LIMIT = 5
ADMIN_SENDER_ID = 'support@campusfeedapp.com'