#!/usr/bin/python3
"""module that contains view funcs for place"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route("/places/<place_id>", strict_slashes=False, 
                 methods=['GET', 'DELETE', 'PUT'])
def manipulate_cities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        return {}, 200

    if request.method == 'PUT':

        try:
            http = request.get_json()
        except Exception:
            return "Not a JSON", 400

        # creating list of attr to ignore in loop
        ignored_attr = ['id', 'user_id', 'created_at', 'updated_at', 'city_id']

        # iterating through dict
        for key, value in http.items():

            # skipping if key in ignore list
            # least, that's what i hope continue does
            if key not in ignored_attr:
                setattr(place, key, value)

            # updating place dictionary
            # which saves in the place object right?

        place.save()

    # returning place object
    return jsonify(place.to_dict()), 200

@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                  methods=['POST'])
def create_place(city_id):

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # uses get_json to parse http_body into dict
    http = request.get_json(silent=True)

    # get_json returns None if it fails
    if http is None:
        abort(400, 'Not a JSON')

    # checks if name is in http dict
    if 'user_id' not in http:
        abort(400, 'Missing user_id')

    if 'name' not in http:
        abort(400, 'Missing name')

    user = storage.get(User, http.get('user_id'))
    if user is None:
        abort(404)
    
    # adds state_id to http dict
    http.update({"city_id": city_id})

    # init new city with http dict
    place = Place(**http)

    # performs new on object, updates and saves with
    # Basemodel save method
    place.save()

    # returns jsonified dict of city object
    return jsonify(place.to_dict()), 201
        