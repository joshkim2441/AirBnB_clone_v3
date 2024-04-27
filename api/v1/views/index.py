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


@app_views.route('/status')
def api_status():
    """ Status of the API """
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each object by type """
    if request.method == 'GET':
        num_objs = {}
        NAMES = {
            "Amenity": "amenities",
            "City": "cities",
            "Places": "places",
            "Reviews": "reviews",
            "States": "states",
            "Users": "users"
        }

    for i, value in NAMES.items():
        num_objs[value] = storage.count(i)

    return jsonify(num_objs)
