#!/usr/bin/python
"""Flask App"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

# Create a Flask instance
app = Flask(__name__)
app.register_blueprint(app_views)

# Get host and port from environment variables or use default values
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', 5000)


# Define a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


# Define a method to handle 404 errors
@app.errorhandler(404)
def not_found(err):
    """Handles 404 errors and returns
    a JSON-formatted 404 status code response"""

    return jsonify({"error": "Not found"}), 404


# Run the Flask server if the script is executed directly
if __name__ == '__main__':
    """Run the Flask server"""
    app.run(host=host, port=port, threaded=True)
