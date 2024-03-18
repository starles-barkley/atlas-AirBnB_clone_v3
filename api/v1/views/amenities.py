#!/usr/bin/python3

'''Creates view for amenity objects'''

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import index
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''Gets all amenities'''
    amenities = [amenity.to_dict() for amenity in Amenity.query.all()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    '''Get amenity by using id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes an amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''creates an amenity'''
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    latest_amenity = Amenity(**HTTP_body)
    storage.new(latest_amenity)
    storage.save()
    return jsonify(latest_amenity.to_dict()), 201

