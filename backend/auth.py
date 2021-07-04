import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
  create_access_token,
  get_jwt_identity,
  jwt_required,
)
from marshmallow.exceptions import ValidationError

import models
from models import User
from schemas import UserSchema

auth = Blueprint('auth', __name__)

def pw_hash(pw):
  return bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())

# --- Auth --- #
@auth.route("/login", methods=["POST"])
def login():
  email = request.json.get("email", None)
  password = request.json.get("password", None)

  try:
    user = User.select().where(User.email == email).get()
  except:
    return jsonify({"message": "Bad email or password"}), 401

  if bcrypt.checkpw(password.encode('utf-8'), user.passwordHash.encode('utf-8')):
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token, user=UserSchema().dump(user))

  return jsonify({"message": "Bad email or password"}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
  user_id = get_jwt_identity()
  print(user_id)
  access_token = create_access_token(identity=user_id)
  return jsonify(access_token=access_token)


@auth.route('/verify', methods=['POST'])
@jwt_required()
def verify_token():
    try:
      current_user = get_jwt_identity()
      user = User.select().where(User.id == current_user).get()
      return jsonify({'success': True, 'user': UserSchema().dump(user)}), 200
    except models.UserDoesNotExist:
      return jsonify({'success': False}), 401

@auth.route("/register", methods=["POST"])
def register():
  json_input = request.json

  try:
    data = UserSchema().load(json_input)
  except ValidationError as err:
    return {"errors": err.messages}, 422
  try:  # Use get to see if user already exists
    User.get(User.email == data["email"])
  except User.DoesNotExist:
    hashedPassword = pw_hash(data.get('password'))
    user = User.create(
      name=data.get('name'),
      email=data.get('email'),
      passwordHash=hashedPassword
    )
    message = "Successfully created user: {}".format(user.email)
  else:
    print('already registered')
    return jsonify({"errors": "You have already registered"}), 400

  data = UserSchema().dump(user)
  access_token = create_access_token(identity=user.id)
  return {'user': data, 'message': message, 'access_token': access_token}, 201

@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  # Access the identity of the current user with get_jwt_identity
  current_user = get_jwt_identity()
  return jsonify(logged_in_as=current_user), 200