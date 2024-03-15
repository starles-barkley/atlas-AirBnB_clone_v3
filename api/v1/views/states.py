#!/usr/bin/python3

'''Creates view for state objects'''

from flask import Flask, jsonify, abort, request
from models import state
from api.v1.views import index

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = State.all()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = State.get(state_id)
    if state is None:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201
