""" 
Functions to implement push messaging.
"""
import logging
import json
import urllib2
import time
from util.const import GCM_PUSH_MESSAGE_API_KEY_MOBILE
from util.const import GCM_PUSH_MESSAGE_API_KEY
from util.const import DRIVER_PUSH_TIME_TO_LIVE_BOOKING

def push(json_data):
    """ Push given json(dict) data and send to google gcm server """
    url = 'https://android.googleapis.com/gcm/send'
    myKey = GCM_PUSH_MESSAGE_API_KEY #key for blowhorntest
    #logging.info('Sending push message with API key :' + myKey)
    data = json.dumps(json_data)
    headers = {'Content-Type': 'application/json', 'Authorization': 'key=%s' % myKey}
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    #logging.info('Push response below')
    #TODO: if canonical_ids is valid, the gcm registration id needs to be updated in the DB
    logging.info(json.dumps(response,sort_keys=True, indent=2))

def push_to_client(json_data):
    url = 'https://android.googleapis.com/gcm/send'
    myKey = GCM_PUSH_MESSAGE_API_KEY_MOBILE #key for BlowhornApp
    #logging.info('Sending push message with API key :' + myKey)
    data = json.dumps(json_data)
    headers = {'Content-Type': 'application/json', 'Authorization': 'key=%s' % myKey}
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    #logging.info('Push response below')
    #TODO: if canonical_ids is valid, the gcm registration id needs to be updated in the DB
    logging.info(json.dumps(response,sort_keys=True, indent=2))

def push_single_message(gcm_id, message):
    #logging.info('Pushing message to GCM ID: %s' % gcm_id)
    json_data = {
        #"collapse_key" : "msg", 
        "data" : {
            "message" : message,
        },
        "registration_ids": [gcm_id],
        "time_to_live" : DRIVER_PUSH_TIME_TO_LIVE_BOOKING,
    }
    push(json_data)

def push_dict(gcm_id, dict_, ttl=DRIVER_PUSH_TIME_TO_LIVE_BOOKING):
    #logging.info('Pushing message to GCM ID: %s' % gcm_id)
    json_data = {
        #"collapse_key" : "msg", 
        "data" : {
            "message" : dict_,
        },
        "registration_ids": [gcm_id],
        "time_to_live" : ttl,
    }
    push(json_data)

def push_status(gcm_id, dict_):
    json_data = {
        "data" : dict_,
        "registration_ids": [gcm_id],
        "time_to_live" : DRIVER_PUSH_TIME_TO_LIVE_BOOKING,
    }
    push_to_client(json_data)
