import logging
import webapp2
import random
import string
import json
from datetime import datetime, timedelta
from db.database import Users, DBMobileAuth, DBUserGCMId
from google.appengine.api import users
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class ForgotPassword(BaseHandler, webapp2.RequestHandler):