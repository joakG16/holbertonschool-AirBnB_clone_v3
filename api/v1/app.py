#!/usr/bin/python3
""" Flask app inizialization """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0") # CORS instance allowing: /* for 0.0.0.0


@app.teardown_appcontext
def close_func(exit):
    storage.close()


@app.errorhandler(404)
def error_404(error):
    ''' Return error status code and message in JSON format '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(port=port, host=host, threaded=True, debug=True)
