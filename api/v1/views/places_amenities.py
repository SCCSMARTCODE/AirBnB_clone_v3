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
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if db == 'db':
        plamenities = place.amenities
    else:
        plamenities = place.amenity_ids

    if amenity not in plamenities:
        abort(404)

    plamenities.remove(amenity)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if db == 'db':
        plamenities = place.amenities
    else:
        plamenities = place.amenity_ids

    if amenity in plamenities:
        return jsonify(amenity.to_dict())

    plamenities.append(amenity)
    place.save()  # Save the Place object to persist changes

    return jsonify(amenity.to_dict()), 201
