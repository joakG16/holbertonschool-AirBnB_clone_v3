#!/usr/bin/python3
''' a new view for State objects that handles all default RESTFul API
actions '''
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    ''' retrieve a list of of all State object '''
    states_list = [stat.to_dict() for stat in storage.all(State).values()]
    # retrieve the state objects using all method and then values(), and
    # convert it into a dictionary each for JSON representation
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    ''' retrieve a State obj depending on its id '''
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)  # returns 404 error
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_index(state_id):
    ''' delete a state obj based on it's id '''
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)  # returns 404 error
    storage.delete(obj)
    storage.save()  # changes need to be saved
    return jsonify({}), 200  # HTTP 200 OK success status response code


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    state_data = request.get_json()
    # Transform the HTTP body request to a dictionary
    # None is returned in case data passed is not "jsonifible"
    if state_data is None:
        abort(400, "Not a JSON")
    if 'name' not in state_data:
        abort(400, "Missing Name")
    new_state = State(**state_data)  # creating the new state object
    # with its unpacked data (in key-value pairs) as kwargs
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
    # 201: Created success status response code indicates that the request
    # has succeeded and has led to the creation of a resource


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    ''' update a state object '''
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
