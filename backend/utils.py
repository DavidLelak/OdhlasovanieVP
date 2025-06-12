from flask import request

def get_current_user():
    user = getattr(request, "user", None)
    if not user:
        return None
    return {"username": user.username, "is_admin": user.is_admin}
