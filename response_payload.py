import json
from flask import make_response, jsonify

def response(status,data):
    if status > 300:
        result = {
        'status' : "error",
        'messages' : data
        }
        return make_response(jsonify(result),status)
    else:
        result = {
            'status' : 'sukses',
            'data' : data
        }
        return make_response(jsonify(result),status)