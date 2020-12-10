import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user
user = Blueprint('users', 'user')

@user.route('/', methods=["GET"])
def test_user_resource():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        return jsonify(data=users, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})
    return "user resource works"

@user.route('/register/', methods=["POST"])
def register():
    payload = request.get_json()
    payload["username"] = payload["username"].lower()
    try:
        models.User.get(models.User.username == payload["username"])
        return jsonify(
            data={},
            message=f"{payload['username']} already exists. Choose another username",
            status=401
        ), 401
    except models.DoesNotExist:
        pw_code = generate_password_hash(payload["password"])
        create_user = models.User.create(
            username=payload["username"],
            password=pw_code
        )
        create_user_dict = model_to_dict(create_user)
        login_user(create_user)
        create_user_dict.pop('password')
        return jsonify(
            data=create_user_dict,
            message=f"{create_user_dict['username']} successfully registered",
            status=201
        ), 201

@user.route('/login/', methods=["POST"])
def login():
    payload = request.get_json()
    payload["username"]=payload["username"].lower()
    try:
        user = models.User.get(models.User.username == payload["username"])
        user_dict = model_to_dict(user)
        password_correct = check_password_hash(user_dict["password"], payload["password"])
        if(password_correct):
            login_user(user)
            user_dict.pop('password')
            return jsonify(
                data=user_dict,
                message=f"{user_dict['username']} successfuly logged in",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="Username or password is incorrect",
                status=401
            ), 401
    except models.DoesNotExist:
        return jsonify(
            data={},
            message="Username or password is incorrect",
            status=401
        ), 401

@user.route('/logout/', methods=["GET"])
def logout():
    logout_user()
    return jsonify(data={}, status={'code': 200, 'message': 'successful logout'})