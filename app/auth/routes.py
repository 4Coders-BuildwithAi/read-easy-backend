from flask import Blueprint, jsonify, request, abort
from app.db.schema import User
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login_user():
    body = request.get_json()
    
    passw = body["password"]

    user = User.query.filter(User.email == body["email"]).first()
    print(body)

    if user and check_password_hash(user.password, passw):
        return jsonify(
            {
                "success": True,
                "name": body["username"],
                "email": body["email"],
                "role": body["role"],
                "id": user.id,
            }
        )
    else:
        return {"message": "User doesn't exists"}

@auth.route("/signup", methods=["POST"])
def signup_user():
    body = request.get_json()
    new_user = User(body["username"], body["email"],body["password"], body["role"])
    new_user.insert()
    return jsonify(
            {
                "success": True,
                "name": body["username"],
                "email": body["email"],
                "role": body["role"],
                "id": new_user.id,
            }
        )
    
