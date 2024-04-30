#!/usr/bin/python3
""" A new view for State object """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
        states route to handle http method for requested
        states no id provided
    """
    if request.method == 'GET':
        all_states = storage.all(State).values()
        list_states = [state.to_dict() for state in all_states]

        return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
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
        abort(404, description='Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        abort(404, description='Missing name')

    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        states route to create a new state
    """
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
