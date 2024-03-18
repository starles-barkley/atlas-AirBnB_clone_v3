#!/usr/bin/python3

'''Creates view for amenity objects'''

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import index
from api.v1.views import app_views
from models.review import Reviews
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_reviews():
    '''Gets all reviews of a specific place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    '''Get review by using id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    '''Deletes a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    '''creates a review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(400)
    HTTP_body = request.get_json()
    if not HTTP_body:
        abort(400, 'Not a json')
    if 'user_id' not in HTTP_body:
        abort(400, 'Missing user_id')
    user = storage.get(User, HTTP_body['user_id'])
    if not user:
        abort(404)
    if 'text' not in HTTP_body:
        abort(400, 'Missing text')
    latest_review = Review(**HTTP_body)
    storage.new(latest_review)
    storage.save()
    return jsonify(latest_review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews(review_id):
    '''Updates a review'''
    HTTP_body = request.get_json(silent=True)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not HTTP_body:
        abort(400, "Not a JSON")
    for key, value in HTTP_body.items():
        if key not in [
            "id", "user_id", "place_id" "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
