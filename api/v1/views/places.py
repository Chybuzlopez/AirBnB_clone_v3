#!/usr/bin/python3
""" places file """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, City, Place, User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, 'Missing name')
    place = Place(**request.json)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Search for Place objects based on request JSON
    """
    request_json = request.get_json()
    if request_json is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = request_json.get('states')
    cities = request_json.get('cities')
    amenities = request_json.get('amenities')

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    if states:
        state_places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city.id not in cities:
                        cities.append(city.id)
                state_places.extend(state.places)
        places = state_places

    if cities:
        city_places = []
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                city_places.extend(city.places)
        places = city_places

    if amenities:
        amenity_places = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if set(amenities).issubset(set(place_amenities)):
                amenity_places.append(place)
        places = amenity_places

    return jsonify([place.to_dict() for place in places])

