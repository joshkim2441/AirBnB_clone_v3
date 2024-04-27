#!/usr/bin/python3
""" Creating the flask app, app_views"""
from api.v1.views import app_views
from flask import jsonify
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
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities",
             "cities",
             "places",
             "reviews",
             "states",
             "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
