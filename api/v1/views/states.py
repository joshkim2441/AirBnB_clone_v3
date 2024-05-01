#!/usr/bin/python3
""" A new view for State object """
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
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
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states(state_id):
    """
        states route to delete state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
        states route to create a new state
    """
    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        abort(400, description='Missing name')

    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        states route to create a new state
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
