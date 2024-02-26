#!/usr/bin/python3
"""Cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_states(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    cities = list(city.to_dict() for city in state.cities)
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_by_id(city_id):
    """Handles Cities requests"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'Not a JSON')
        city.name = data.get('name', city.name)
        city.save()
        return jsonify(city.to_dict()), 200

    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
