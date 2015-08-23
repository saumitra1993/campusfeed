import webapp2
import logging
from service._users.sessions import BaseHandler
from db.database import DBMobileAuth,DBUserGCMId, Users
from google.appengine.ext import ndb

class LogoutUser(BaseHandler, webapp2.RequestHandler):
    def get(self):
        if self.userid:
            try:
                del self.session['user']
            except: pass
            try:
                del self.session['userid'] 
            except: pass
            try:
                del self.session['name'] 
            except: pass
        elif self.request.headers.get("token"):
            mobile_entry = DBMobileAuth.get_by_id(self.request.headers.get("token"))
            user_id = mobile_entry.user_id
            logging.info(user_id)
            user_id = int(user_id)
            user = Users.get_by_id(user_id)
            user_ptr = user.key
            gcm = DBUserGCMId.query(DBUserGCMId.user_ptr == user_ptr).fetch()
            key_ = gcm[0].key
            key_.delete()
            key = mobile_entry.key
            key.delete()
        self.response.set_status(200, 'Awesome')