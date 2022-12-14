from main import app
import json


def error(message):
    response = app.response_class(
        json.dumps({"message":message}),
        status=404,
        mimetype='application/json'
    )
    return response

def response(res):
    response = app.response_class(
        json.dumps(res,default=str),
        status=200,
        mimetype='application/json'
    )
    return response
