#!/usr/bin/python
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
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }

    for key, value in classes.items():
        count = storage.count(value)
        counts[key] = count

    return jsonify(counts)
