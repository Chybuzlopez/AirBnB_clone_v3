#!/usr/bin/python3
""" app file """

import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_storage(exception):
    """Closes the storage engine on teardown"""
    storage.close()

# Define a handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)

