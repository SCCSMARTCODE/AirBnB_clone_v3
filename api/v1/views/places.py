#!/usr/bin/python3
"""Place"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_by_city(city_id):
    """retrievs places in a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = list(place.to_dict() for place in city.places)
        return jsonify(places)
    if request.method == 'POST':
        if request.get_json(silent=True) is None:
            abort(400, 'Not a JSON')
        if not storage.get(City, city_id):
            abort(404)
        if 'user_id' not in request.get_json(silent=True):
            abort(400, 'Missing user_id')
        usr = storage.get(User, request.get_json(silent=True)['user_id'])
        if usr is None:
            abort(404)
        if 'name' not in request.get_json(silent=True):
            abort(400, 'Missing name')
        data = request.get_json(silent=True)
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place_by_id(place_id=None):
    """retrieves place obj by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        places_json = request.get_json(silent=True)
        if not places_json:
            abort(400, 'Not a JSON')
        keylist = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in places_json.items():
            if k not in keylist:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict())
