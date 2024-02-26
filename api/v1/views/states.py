#!/usr/bin/python3
"""States"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """Retrieves the list of all State objects:"""
    states = storage.all(State)
    all_states = list(obj.to_dict() for obj in states.values())
    return jsonify(all_states)

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT'],
                 strict_slashes=False)
def list_states(state_id=None):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not found")

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state route
    :return: newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
