#!/usr/bin/python3
"""module that contains view funcs for city"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
def get_cities(state_id=None):
    from models import storage
    from models.state import State
    from models.city import City
    if state_id is None:
        abort(404)
    if request.method == 'GET':
        state = storage.get(State, state_id)
        all_cities = state.cities
        return jsonify([city.to_dict() for city in all_cities])
    if request.method == 'POST':
        try:
            http = request.get_json()
        except Exception:
            return "Not a JSON", 400
        try:
            name = http.get("name")
        except Exception:
            abort(400)
        try:
            state = storage.get(State, state_id)
        except Exception:
            abort(404)
        city = City(state_id=state_id, name=name)
        storage.new(city)
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['GET', 'PUT'])
def get_city(city_id=None):
    from models import storage
    from models.city import City
    
    # checking if city_id is None
    if city_id is None:
        abort(404)
    # checking if city_id is connected to City
    city = storage.get(City, city_id)
    if city is None:
            abort(404)
    if request.method == 'GET':
        # basic get request, json the object dict
        return jsonify(city.to_dict())
    if request.method == 'PUT':
        # seeing if HTTP body is dict
        try:
            http = request.get_json()
        except Exception:
            return "Not a JSON", 400
        
        # creating list of attr to ignore in loop
        ignored_attr = ['id', 'state_id', 'created_at', 'updated_at']
        
        # iterating through dict
        for key, value in http.items():
            
            # skipping if key in ignore list
            # least, that's what i hope continue does
            if key in ignored_attr:
                continue

            # updating city dictionary
            # which saves in the city object right?
            city.__dict__.update({key: value})

    # returning city object        
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=['DELETE'])
def destroy_state(city_id=None):
    from models import storage
    from models.city import City
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return {}, 200


# @app_views.route("/cities/<city_id>", methods=['PUT'])
# def create_state(state_id=None):
#     pass
