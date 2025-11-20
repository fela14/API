import jwt
import datetime
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "missing credentials"}), 401

    # check db for username and password