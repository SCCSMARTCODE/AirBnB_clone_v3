#!/usr/bin/python3
"""User"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def users(user_id):
    """retrieves user by id, or all users"""
    if user_id is None:
        users = storage.all(User)
        all_users = list(user.to_dict() for user in users.values())
        return jsonify(all_users)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(user.to_dict())


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
<<<<<<< HEAD
    """handle POST requests"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json(silent=True)
=======
    """handle PUT requests"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json(silent=True, force=True)
>>>>>>> 22e838829dbc0419b3ce3df702f817ec257bdc99
    if not data:
        abort(400, 'Not a JSON')
    user.password = data.get('password', user.password)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def delete_user(user_id):
    """handles DELETE request"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
