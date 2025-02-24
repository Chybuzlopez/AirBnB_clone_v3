#!/usr/bin/python3
"""View for the link between Place objects and Amenity objects that handles
all default RESTFul API actions.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object from a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Links a Amenity object to a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

