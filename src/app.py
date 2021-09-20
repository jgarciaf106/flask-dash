"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
#from models import Person

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
server = Flask(__name__)
server.url_map.strict_slashes = False
app = dash.Dash(__name__, server=server)

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

# Dash Call Backs
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.H1(children="Test Div"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    server.run(host='0.0.0.0', port=PORT, debug=True)