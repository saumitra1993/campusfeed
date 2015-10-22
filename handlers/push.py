""" 
Functions to implement push messaging.
"""
import logging
import json
import urllib2
import time
from const.constants import GCM_PUSH_MESSAGE_API_KEY_MOBILE
from const.constants import GCM_PUSH_MESSAGE_API_KEY

def push(json_data):
    """ Push given json(dict) data and send to google gcm server """
    url = 'https://pushy.me/push?api_key=def7829fa62917c90b2e217773d1650cf80a2d1378ec2ddb03cfa40b7a88b67b'
    #myKey = GCM_PUSH_MESSAGE_API_KEY #key for blowhorntest
    #logging.info('Sending push message with API key :' + myKey)
    data = json.dumps(json_data)
    headers = {'Content-Type': 'application/json'}#, 'Authorization': 'key=%s' % myKey#
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    #logging.info('Push response below')
    #TODO: if canonical_ids is valid, the gcm registration id needs to be updated in the DB
    logging.info(json.dumps(response,sort_keys=True, indent=2))

def push_old(json_data):
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

def push_special(json_data):
    """ Push given json(dict) data and send to google gcm server """
    url = 'https://pushy.me/push?api_key=711b4dcfe7d2afa385d61ffe364cc7675ef9e60dcce51047405bac4b467d5ef1'
    #myKey = GCM_PUSH_MESSAGE_API_KEY #key for blowhorntest
    #logging.info('Sending push message with API key :' + myKey)
    data = json.dumps(json_data)
    logging.info(data)
    headers = {'Content-Type': 'application/json'}#, 'Authorization': 'key=%s' % myKey#
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

def push_dict(gcm_id, dict_):
    if "message" in dict_:
        json_data = {
            #"collapse_key" : "msg", 
            "data" : {
                "message" : dict_,
            },
            "registration_ids": [gcm_id],
        }
        push_special(json_data)
    elif len(gcm_id) > 22:
        logging.info('Pushing message to GCM ID: %s' % gcm_id)
        json_data = {
            #"collapse_key" : "msg", 
            "data" : {
                "message" : dict_,
            },
            "registration_ids": [gcm_id],
        }
        push_old(json_data)

    else:
        logging.info('Pushing message to pushy ID: %s' % gcm_id)
        json_data = {
            #"collapse_key" : "msg", 
            "data" : {
                "message" : dict_,
            },
            "registration_ids": [gcm_id],
        }
        push(json_data)

def push_status(gcm_id, dict_):
    json_data = {
        "data" : dict_,
        "registration_ids": [gcm_id],
        "time_to_live" : DRIVER_PUSH_TIME_TO_LIVE_BOOKING,
    }
    push_to_client(json_data)
