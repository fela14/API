import jwt
import datetime
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

server = Flask(__name__)
mysql = MySQL(server)

# Config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))
server.config["MYSQL_CURSORCLASS"] = "DictCursor"

JWT_SECRET = os.environ.get("JWT_SECRET", "supersecretkey")


def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "admin": is_admin,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "missing credentials"}), 401

    # Check database for user
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res == 0:
        cur.close()
        return jsonify({"message": "invalid credentials"}), 401

    user_row = cur.fetchone()
    cur.close()

    # Compare hashed password
    if not bcrypt.checkpw(auth.password.encode(), user_row["password"].encode()):
        return jsonify({"message": "invalid credentials"}), 401

    # Generate JWT
    token = createJWT(auth.username, JWT_SECRET, True)
    return jsonify({"token": token}), 200


@server.route("/validate", methods=["POST"])
def validate():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "missing credentials"}), 401

    # Handle Bearer token
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"message": "invalid token format"}), 401

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return jsonify({"message": "decoded", "user": decoded}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "not authorized"}), 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
