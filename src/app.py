"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.dash import dash_app
#from models import Person

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
server = Flask(__name__)
server.url_map.strict_slashes = False

# database condiguration
if os.getenv("DATABASE_URL") is not None:
    server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    server.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(server, db)
db.init_app(server)

# Allow CORS requests to this API
CORS(server)

# add the admin
setup_admin(server)

# Add all endpoints form the API with a "api" prefix
server.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object
@server.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@server.route('/site_map')
def sitemap():
    if ENV == "development":
        return generate_sitemap(server)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@server.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

# render dash app
dash_app(server)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    server.run(host='0.0.0.0', port=PORT, debug=True)