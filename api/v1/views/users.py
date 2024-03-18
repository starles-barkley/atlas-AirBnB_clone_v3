#!/usr/bin/python3

'''Creates view for user objects'''

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import index
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''Gets all users'''
    users = storage.all(User).values()
    list_of_users = [user.to_dict() for user in users]
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    '''Get user by using id'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Deletes a user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''creates a user'''
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'email' not in HTTP_body:
        abort(400, 'Missing email')
    if 'password' not in HTTP_body:
        abort(400, 'Missing password')
    latest_user = User(**HTTP_body)
    storage.new(latest_user)
    storage.save()
    return jsonify(latest_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_users(user_id):
    '''Updates a user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, "Not a JSON")
    for key, value in HTTP_body.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
