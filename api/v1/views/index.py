#!/usr/bin/python3
''' index module '''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    ''' View function that returns the JSON response status '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    ''' Endpoint that retrieves/returns the number of each object
    by type.
    '''
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    obj_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(obj_count)
