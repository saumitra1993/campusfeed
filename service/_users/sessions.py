import webapp2
import logging
import json
from webapp2_extras import sessions
from google.appengine.api import users
from const.messages import KEY_STATUS, KEY_MESSAGE, UNAUTHORIZED, FAIL
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS
from datetime import datetime
from db.database import DBMobileAuth
from const.business import customers

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend = 'datastore')

    @webapp2.cached_property
    def userid(self):
        # Returns the userid
        return self.session.get('userid')

    @webapp2.cached_property
    def user(self):
        # Returns the name of the user
        return self.session.get('name') or self.session.get('user')

    @webapp2.cached_property
    def name(self):
        # Returns the name of the user
        return self.user

    def _unauthorized(self):
        self.response.set_status(400)
        dict_ = {
            KEY_STATUS : UNAUTHORIZED,
            KEY_MESSAGE : UNAUTHORIZED,
        }
        
        self.response.write(json.dumps(dict_))

class LoginRequired(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        obj = self.obj
        token = obj.request.headers.get("token")
        if obj.session.get('userid') is not None:
            r = self.f(obj, *args, **kwargs)
            return r
        elif token:
            customer = customers.get(token)
            if customer:
                obj.session['userid'] = customer.get('userid')
                obj.session['name'] = customer.get('name')
                r = self.f(obj, *args, **kwargs)
                return
            _user = DBMobileAuth.get_by_id(token)
            if _user:
                now = datetime.now()
                if _user.expiration > now:
                    if (_user.expiration - now).total_seconds() < 3600*24:
                        _user.expiration = now + datetime.timedelta(days=MOBILE_USER_SESSION_DURATION_DAYS)
                        _user.put()
                    obj.session['userid'] = _user.user_id
                    obj.session['name'] = _user.name
                    r = self.f(obj, *args, **kwargs)
                    return r
                else:
                    key = _user.key
                    key.delete()

        obj.response.set_status(400)
        dict_ = {
            KEY_STATUS : UNAUTHORIZED,
            KEY_MESSAGE : UNAUTHORIZED,
        }
    
        obj.response.write(json.dumps(dict_))

    def __get__(self, instance, owner):
        self.cls = owner
        self.obj = instance
        return self.__call__
