import webapp2
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
            user_ptr = ndb.Key('Users',user_id)
            gcm = DBUserGCMId.query(DBUserGCMId.user_ptr == user_ptr)
            key_ = gcm.key
            key_.delete()
            key = mobile_entry.key
            key.delete()
        self.response.set_status(200, 'Awesome')