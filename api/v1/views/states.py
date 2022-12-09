#!/usr/bin/python3
''' a new view for State objects that handles all default RESTFul API
actions '''

from flask import jsonify, abort, request
from models import FileStorage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    ''' retrieve a list of of all State object '''
    states_dict = [st.to_dict() for st in FileStorage.all(State).values()]
    # retrieve the state objects using all method, and then
    # convert it into a dictionary each for JSON representation
    return jsonify(states_dict)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    ''' retrieve a State obj depending on its id '''
    obj = FileStorage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)  # returns 404 error

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_by_index(state_id):
    ''' delete a state obj based on it's id '''
    obj = FileStorage.get(State, state_id)
    if obj is None:
        abort(404)  # returns 404 error
    FileStorage.delete(obj)
    FileStorage.save()  # changes need to be saved
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    state_data = request.get_json()  # None in case data passed is
    # not "jsonifible"
    # Transform the HTTP body request to a dictionary
    if state_data is None:
        abort(400, "Not a JSON")
    if state_data['name'] is None:
        abort(400, "Missing Name")
    new_state = State(**state_data)  # creating the new state object
    # with its unpacked data (in key-value pairs) as kwargs
    FileStorage.new(new_state)
    FileStorage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    ''' update a state object '''
    state_obj = FileStorage.get(State, state_id)
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
    FileStorage.save()
    return jsonify(state_obj.to_dict()), 200
