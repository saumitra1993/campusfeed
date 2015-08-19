import webapp2
from service._users.sessions import BaseHandler
from db.database import DBMobileAuth

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
            user = DBMobileAuth.get_by_id(self.request.headers.get("token"))
            key = user.key
            key.delete()
        self.response.set_status(200, 'Awesome')