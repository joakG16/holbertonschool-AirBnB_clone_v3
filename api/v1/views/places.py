#!/usr/bin/python3
''' a new view for Places objects that handles all default RESTFul API
actions '''

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places_by_city(city_id):
    ''' Function that retrieves all Places objects depending
    on the City id given as parameter
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    ''' Function to retrive and return a Place object
    given its id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_obj_by_id(place_id):
    ''' Function to delete a Place object from storage
    given its id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_create_place_object(city_id):
    ''' Post(create) a new Place object and assign its
    correspondent City id.
    City and User will be checked to ensure if
    the ones given in the request exist in storage
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_data_dict = request.get_json()
    if place_data_dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in place_data_dict:
        abort(400, "Missing user_id")

    user = storage.get(User, place_data_dict['user_id'])
    if user is None:
        abort(404)

    if 'name' not in place_data_dict:
        abort(400, "Missing Name")

    place_data_dict['city_id'] = city_id
    new_place = Place(**place_data_dict)

    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_update_place_obj(place_id):
    ''' update Place instance's atributes given through JSON format
    (HTTP body request)
    '''
    place_to_update = storage.get(Place, place_id)
    if place_to_update is None:
        abort(404)
    updated_place_data_dict = request.get_json()
    if updated_place_data_dict is None:
        abort(400, "Not a JSON")
    for key, value in updated_place_data_dict.items():
        if key == 'id' or key == 'user_id' or key == 'city_id'\
             or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(place_to_update, key, value)
    storage.save()
    return jsonify(place_to_update.to_dict()), 200
