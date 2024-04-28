#!/usr/bin/python3
""" A new view for State object """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models import storage, CNC
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
        states route to handle http method for requested states no id provided
    """
    if request.method == 'GET':
        all_states = storage.all(State).values()
        list_states = [state.to_dict() for state in all_states]

        return jsonify(list_states)

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):

    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_states(state_id):
    """
        states route to delete state
    """
    state = storage.get('State', 'state_id')
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
        states route to create a new state
    """

    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')

    if not request.get_json():
        return jsonify(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return abort(404, 'Missing name')

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        states route to create a new state
    """

    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')

    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items:
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
