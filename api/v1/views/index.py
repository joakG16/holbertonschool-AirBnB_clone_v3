#!/usr/bin/python3
''' index module '''
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status')
def status():
    ''' view function that returns the JSON response status '''
    return jsonify({"status": "OK"})