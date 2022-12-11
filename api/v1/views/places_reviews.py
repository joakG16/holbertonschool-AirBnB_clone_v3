#!/usr/bin/python3
''' a new view for Review objects that handles all default RESTFul API
actions '''

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_a_place_reviews_obj(place_id):
    ''' Function to retrieve all Review objects depending
    on the place id given as parameter
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_review_obj_by_id(review_id):
    ''' Function that retrives any review object
    from storage depending on the id requested/given
    '''
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_obj_by_id(review_id):
    ''' Function to delete a Review object from storage
    given its id
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_create_review_object(place_id):
    ''' Post(create) a new Review object and assign its
    correspondent Place id.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_data_dict = request.get_json()
    if review_data_dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in review_data_dict:
        abort(400, "Missing user_id")

    user = storage.get(User, review_data_dict['user_id'])
    if user is None:
        abort(404)

    if 'text' not in review_data_dict:
        abort(400, "Missing Text")

    review_data_dict['place_id'] = place_id
    new_review = Review(**review_data_dict)

    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_update_review_obj(review_id):
    ''' update Review object's atributes given through JSON format
    (HTTP body request)
    '''
    review_to_update = storage.get(Review, review_id)
    if review_to_update is None:
        abort(404)
    updated_review_data_dict = request.get_json()
    if updated_review_data_dict is None:
        abort(400, "Not a JSON")
    for key, value in updated_review_data_dict.items():
        if key == 'id' or key == 'user_id' or key == 'place_id'\
             or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(review_to_update, key, value)
    storage.save()
    return jsonify(review_to_update.to_dict()), 200
