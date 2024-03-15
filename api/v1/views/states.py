#!/usr/bin/python3

'''Creates view for state objects'''

from flask import Flask, jsonify, abort, request
from models import state, storage
from api.v1.views import index
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Gets a state'''
    states = State.all()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State'''
    state = State.get(state_id)
    if state is None:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''creates a state'''
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    '''Updates a state'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
