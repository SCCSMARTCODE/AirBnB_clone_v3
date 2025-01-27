#!/usr/bin/python3
"""Flask framework"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON"""

    jsn = {"status": "OK"}
    return jsonify(jsn)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type:"""

    counts = {}
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }

    for key, value in classes.items():
        count = storage.count(value)
        counts[key] = count

    return jsonify(counts)
