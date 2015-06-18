import webapp2
import logging
from login import Login
from image_url import ImageUrl
from get_photo import GetPhotu
from get_my_channels import GetMyChannels

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'qwertyuioppoiuytrewqqwertyuiopsdfkjbsdjf'
}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
    #Services
    #('/', MyClassName),
    ('/login',Login),
    ('/imageurl',ImageUrl),
    ('/pic/(.*)',GetPhotu),
    ('/users/(.*)/channels',GetMyChannels),
], config=config, debug=True)