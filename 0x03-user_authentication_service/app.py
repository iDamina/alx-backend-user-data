#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """
    Return a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Register a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # regsiter user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Login a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    try:
        user = AUTH.valid_login(email, password)
        if not user:
            abort(401)

        session_id = AUTH.create_session(user.id)

        response = jsonify({"email": user.email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except Exception as e:
        print(f"Exception occured: {e}")
        abort(401)

@app.route("/sessions", methods=["DELETE"])
def logout():
        """
        Logout a user.
        """
        session_id = request.cookies.get('session_id')

        if not session_id:
            abort(403)

        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)

        AUTH.destroy_session(user.id)
        return redirect('/'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
