import webapp2
import logging
from login import Login

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'qwertyuioppoiuytrewqqwertyuiopsdfkjbsdjf'
}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
    #Services
    #('/', MyClassName),
    ('/login',Login),
], config=config, debug=True)