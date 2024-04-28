#!/usr/bin/python3
""" Creating the flask app, app_views"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def api_status():
    """ Status of the API """
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def api_stats():
    """ Retrieves the number of each object by type """
    if request.method == 'GET':
        num_objs = {}
        for key, value in classes.items():
            num_objs[value] = storage.count(key)

        return jsonify(num_objs)
