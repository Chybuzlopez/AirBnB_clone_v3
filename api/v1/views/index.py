#!/usr/bin/python3
""" index file """

from flask import Flask, jsonify
from api.v1 import app_views
from models import storage

app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    stats = {}
    stats['amenities'] = storage.count('Amenity')
    stats['cities'] = storage.count('City')
    stats['places'] = storage.count('Place')
    stats['reviews'] = storage.count('Review')
    stats['states'] = storage.count('State')
    stats['users'] = storage.count('User')
    return jsonify(stats)

if __name__ == '__main__':
    app.register_blueprint(app_views)
    app.run()

