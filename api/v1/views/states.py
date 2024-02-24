#!/usr/bin/python
"""States"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """Retrieves the list of all State objects:"""
    states = storage.all('State')
    all_states = list(obj.to_dict() for obj in states.values())
    return jsonify(all_states)

@app_views.route('/states/<state_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def list_state_with_id(state_id=None):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, "Not found")

    if request.method == 'GET':
        return jsonify(state.to_dict())
    
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({})
    
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = State(data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
