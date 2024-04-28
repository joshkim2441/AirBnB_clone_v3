#!/usr/bin/python3
""" Creating the flask app, registering the blueprint
app_views to flask instance app
"""
from os import getenv
from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    ''' Closes the storage engine '''
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ Return render_template """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
