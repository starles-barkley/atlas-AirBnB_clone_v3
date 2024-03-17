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
