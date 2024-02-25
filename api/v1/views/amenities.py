#!/usr/bin/python3
"""Amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def list_amenities():
    """retrives all amenities"""
    amenities = storage.all(Amenity)
    all_amenities = list(amnty.to_dict() for amnty in amenities.values())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def amenities_by_id(amenity_id):
    """handles an amenity based on its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        return jsonify({}), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_amen = Amenity(data)
        new_amen.save()
        return jsonify(new_amen.to_dict()), 201

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
