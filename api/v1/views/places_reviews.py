#!/usr/bin/python3

'''Creates view for amenity objects'''

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import index
from api.v1.views import app_views
from models.reviews import Reviews


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    '''Gets all reviews'''
    reviews = []
    for review in storage.all(Reviews).values():
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    '''Get review by using id'''
    review = storage.get(Review, review_id)
    if not amenity:
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
def create_reviews():
    '''creates a review'''
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    latest_review = Review(**HTTP_body)
    storage.new(latest_review)
    storage.save()
    return jsonify(latest_review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews(review_id):
    '''Updates a review'''
    json_data = request.get_json(silent=True)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
