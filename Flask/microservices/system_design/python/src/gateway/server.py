import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)
fs = gridfs.GridFS(mongo.db)

# ----------------------------
# RabbitMQ connection
# ----------------------------
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")  # no credentials
)
channel = connection.channel()
channel.queue_declare(queue="video", durable=True)

# ----------------------------
# LOGIN ENDPOINT
# ----------------------------
@server.route("/login", methods=["POST"])
def login():
    token_data, err = access.login(request)
    if not err:
        return token_data, 200
    else:
        return err

# ----------------------------
# UPLOAD ENDPOINT
# ----------------------------
@server.route("/upload", methods=["POST"])
def upload():
    access_data, err = validate.token(request)
    if err:
        return err

    access_data = json.loads(access_data)

    if not access_data.get("admin"):
        return "not authorized", 401

    if len(request.files) != 1:
        return "exactly 1 file required", 400

    for _, f in request.files.items():
        err = util.upload(f, fs, channel, access_data)
        if err:
            return err

    return "success!", 200

# ----------------------------
# DOWNLOAD ENDPOINT (stub)
# ----------------------------
@server.route("/download", methods=["GET"])
def download():
    return "not implemented", 501

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
