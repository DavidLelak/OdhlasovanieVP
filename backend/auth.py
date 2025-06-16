from flask import request, jsonify
from functools import wraps
from models import User

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify({"error": "Authentication required"}), 401
        user = User.query.filter_by(username=auth.username).first()
        if not user or not user.check_password(auth.password):
            return jsonify({"error": "Invalid credentials"}), 403
        request.user = user
        return f(*args, **kwargs)
    return decorated
