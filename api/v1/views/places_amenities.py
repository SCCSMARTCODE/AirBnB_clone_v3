#!/usr/bin/python3
"""Link with Place & Amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from os import getenv
db = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if db == 'db':
        amenities = list(amnty.to_dict() for amnty in place.amenities)
    else:
        amenities = list(amnty.to_dict() for amnty in place.amenity_ids)
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def alter_amenity(place_id, amenity_id):
    """Altering amenity based on Place"""
    if not storage.get(Place, place_id):
        abort(404)
    if not storage.get(Amenity, amenity_id):
        abort(404)
    if db == 'db':
        plamenities = storage.get(Place, place_id).amenities
    else:
        plamenities = storage.get(Place, place_id).amenity_ids
    for amn in plamenities:
        if amn.id == amenity_id:
            storage.delete(storage.get(Amenity, amenity_id))
            storage.save()
        else:
            abort(404)
    return jsonify[{}], 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    if not storage.get(Place, place_id):
        abort(404)
    if not storage.get(Amenity, amenity_id):
        abort(404)
    if db == 'db':
        plamenities = storage.get(Place, place_id).amenities
    else:
        plamenities = storage.get(Place, place_id).amenity_ids

    if storage.get(Amenity, amenity_id) in plamenities:
        return jsonify(storage.get(Amenity, amenity_id).to_dict())
    plamenities.append(storage.get(Amenity, amenity_id))
    storage.get(Place, place_id).save()
    return jsonify(storage.get(Amenity, amenity_id).to_dict()), 201
