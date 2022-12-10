#!/usr/bin/python3
''' a new view for User objects that handles all default RESTFul API
actions '''

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users_objs():
    ''' Function that retrieves and returns all User instances from storage
    given a GET HTTP request
    '''
    users_list = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_obj_by_id(user_id):
    ''' Function that retrieves and returns a User instance given its id '''
    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404)
    return jsonify(user_object.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_obj_by_id(user_id):
    ''' Function that deletes a User instance from storage given its id '''
    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404)
    storage.delete(user_object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_create_user_obj():
    ''' Function to create a User object in storage '''
    new_user_data_dict = request.get_json()
    if new_user_data_dict is None:
        abort(400, "Not a JSON")
    if 'email' not in new_user_data_dict:
        abort(400, "Missing email")
    if 'password' not in new_user_data_dict:
        abort(400, "Missing password")
    new_user = User(**new_user_data_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_obj_by_id(user_id):
    ''' Function that updates the user's attributes, with a given id and
    updated data
    '''
    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404)
    updated_user_data_dict = request.get_json()
    if updated_user_data_dict is None:
        return(400, "Not a JSON")
    for key, value in updated_user_data_dict.items():
        if key == 'id' or key == 'email' or key == 'created_at'\
             or key == 'updated_at':
            pass
        else:
            setattr(user_object, key, value)
    storage.save()
    return jsonify(user_object.to_dict()), 200
