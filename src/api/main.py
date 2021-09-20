"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

# from models import Person

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
server.url_map.strict_slashes = False
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONNECTION_STRING")
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
MIGRATE = Migrate(server, db)
db.init_app(server)
CORS(server)
setup_admin(server)

# Handle/serialize errors like a JSON object
@server.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@server.route("/site_map")
def sitemap():
    return generate_sitemap(server)


# API Call Backs
@server.route("/user", methods=["GET"])
def handle_hello():

    response_body = {"msg": "Hello, this is your GET /user response "}

    return jsonify(response_body), 200


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
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    server.run(host="0.0.0.0", port=PORT, debug=False)
