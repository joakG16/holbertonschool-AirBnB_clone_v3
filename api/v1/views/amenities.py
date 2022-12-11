#!/usr/bin/python3
''' a new view for Amenity objects that handles all default RESTFul API
actions '''
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    ''' Function that retrieves and returns a list Amenity objects
    currently in Storage, given a GET request
    '''
    amenities_list = [amen.to_dict() for amen in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    ''' Function to retrieve and return an Amenity object searched by its id'''
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    ''' Delete an Amenity object from storage given its id '''
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_create_amenity():
    ''' Create a new Amenity instance given the data as dict. through
    a HTTP body request
    '''
    new_amenity_data_dict = request.get_json()
    if new_amenity_data_dict is None:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity_data_dict:
        abort(400, "Missing name")
    new_amenity = Amenity(**new_amenity_data_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_update_amenity_by_id(amenity_id):
    ''' Update a stored Amenity instance's attributes
    given its id and data (dictionary passed through
    HTTP body request in JSON format)
    '''
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_data_dict = request.get_json()
    if amenity_data_dict is None:
        abort(400, "Not a JSON")
    for key, value in amenity_data_dict.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(amenity_obj, key, value)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
