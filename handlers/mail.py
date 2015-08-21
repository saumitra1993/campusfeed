import os
import datetime
import logging
import urllib
import json

from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext import blobstore
from const.constants import ADMIN_SENDER_ID
import traceback

dev_server = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

#Generic function to send email
def send_email(
    subject,
    to,
    body,
    sender=ADMIN_SENDER_ID,
    attachments = None,
):
    logging.info('Email: to=%s, subject=%s' % (to, subject))
    message = mail.EmailMessage()
    message.sender = sender
    message.to = to
    message.subject = subject
    message.body = body
    if attachments:
        message.attachments = attachments
    message.send()



