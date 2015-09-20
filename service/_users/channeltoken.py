__author__ = 'Saumitra'

import webapp2
import json
import logging
from google.appengine.api import channel
from service._users.sessions import BaseHandler


class ChannelToken(BaseHandler, webapp2.RequestHandler):

    def get(self):
        token = None
        channel_id = self.request.get('channel_id')
        if channel_id:
           token = channel.create_channel(channel_id)
            
        dict_ = {
            'token' : token
        }
        logging.info('token=%s' % token)
        result = json.dumps(dict_)
        self.response.write(result);

