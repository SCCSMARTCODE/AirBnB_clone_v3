"""Review"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_review_by_place(place_id):
    """retrieve the reviews from places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = list(review.to_dict() for review in place.reviews)
        return jsonify(reviews)
    if request.method == 'POST':
        review_json = request.get_json(silent=True)
        if not review_json:
            abort(400, 'Not a JSON')
        if not storage.get(Place, place_id):
            abort(404)
        if 'user_id' not in review_json:
            abort(400, 'Missing user_id')
        user = storage.get(User, review_json['user_id'])
        if not user:
            abort(404)
        if 'text' not in review_json:
            abort(400, 'Missing text')
        new_review = Review(**review_json)
        new_review.save()
        return jsonify(new_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_by_id(review_id):
    """retrieves a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'Not a JSON')
        keylist = ['id', 'user_id', 'place_id', 'city_id',
                   'created_at', 'updated_at']
        for k, v in data.items():
            if k not in keylist:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict())
