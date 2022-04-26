# import json
from flask import make_response, jsonify

def response(status,messages,data = None):
    if status >= 400:
        result = {
        'status' : "error",
        'messages' : messages
        }
        return make_response(jsonify(result),status)
    else:
        result = {
            'status' : 'success',
            'messages' : messages,
            'data' : data
        }
        return make_response(jsonify(result),status)