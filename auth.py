from functools import wraps
import os, sys, json
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'flask'))
from flask import Flask, request, jsonify, Response
from hashlib import sha1
import logging, hmac, base64
from auth_data import app_keys

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #get request info
        verb = request.method
        url = request.url

        #check hmac
        (user_id, message_hmac) = request.headers["Hmac"].split(":")
        content_md5 = request.headers["Content-Md5"]
        datetime = request.headers["Datetime"]
        to_sign = "%s\n%s\n%s\n%s" % (verb, content_md5, datetime, url)
        if not is_equal(message_hmac, calculate_hmac(to_sign)):
            return need_to_authenticate()
        return f(*args, **kwargs)
    return decorated

def is_equal(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= (x != y)
    return result == 0

def calculate_hmac(to_sign):
    hashed = hmac.new(app_keys["app_secret"], to_sign, sha1)
    return base64.b64encode(hashed.digest())

def need_to_authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})