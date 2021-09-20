"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User

api = Blueprint('api', __name__)

# API Call Backs
@api.route("/user", methods=["GET"])
def handle_hello():

    response_body = {"msg": "Hello, this is your GET /user response "}

    return jsonify(response_body), 200

