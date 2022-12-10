#!/usr/bin/python3
''' a new view for City objects that handles all default RESTFul API
actions '''

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    ''' retrieve a list of of all City objects by state id'''
    cities_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    ''' retrieve any City object based on its id'''
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    ''' delete a City object based on its id '''
    city_to_delete = storage.get(City, city_id)
    if not city_to_delete:
        abort(404)
    storage.delete(city_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_create_city(state_id):
    ''' post(create) a new city and assign its correspondent state id '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city_data = request.get_json()
    # Transform the HTTP body request to a dictionary
    # None is returned in case data passed is not "jsonifible"
    if new_city_data is None:
        abort(400, "Not a JSON")
    if 'name' not in new_city_data:
        abort(400, "Missing Name")
    new_city = City(**new_city_data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_by_id(city_id):
    ''' update a City instance's atributes given through JSON format
    (HTTP body request)
    '''
    city_to_update = storage.get(City, city_id)
    if not city_to_update:
        abort(404)
    updated_city_data_dict = request.get_json()
    if updated_city_data_dict is None:
        abort(400, "Not a JSON")
    for key, value in updated_city_data_dict.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(city_to_update, key, value)
    storage.save()
    return jsonify(city_to_update.to_dict()), 200

