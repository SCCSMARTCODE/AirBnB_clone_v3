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


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get(State, state_id):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
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

        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict())
