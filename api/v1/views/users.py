#!/usr/bin/python3
"""User"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users(user_id):
    """retrieves all users"""
    user_list = []
    user_obj = storage.all(User)
    for obj in user_obj.values():
        user_list.append(obj.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    gets User by ID
    """

    obj = storage.get(User, str(user_id))

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """handle POST requests"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new = User(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """handle PUT requests"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json(silent=True, force=True)
    if not data:
        abort(400, 'Not a JSON')

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, val)

    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """handles DELETE request"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
