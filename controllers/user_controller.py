from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from models.temples import Temples
from util.reflection import populate_object
from lib.authenticate import requires_min_rank, authenticate_return_auth, check_ownership_or_rank


def add_user():
  post_data = request.form if request.form else request.json

  required_fields = ['username', 'email', 'password']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  temple_id = post_data.get('temple_id')
  if temple_id:
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    if not temple_query:
      return jsonify({"message": "temple not found"}), 404

  new_user = Users.new_user_obj()
  populate_object(new_user, post_data)

  new_user.password = generate_password_hash(new_user.password).decode('utf8')

  try:
    db.session.add(new_user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to create user"}), 400

  return jsonify({"message": "force user created", "result": user_schema.dump(new_user)}), 201


@requires_min_rank('Council')
def get_all_users(auth_info):
  users_query = db.session.query(Users).all()
  return jsonify({"message": "force users found", "results": users_schema.dump(users_query)}), 200


@authenticate_return_auth
def get_user_profile(auth_info):
  return jsonify({"message": "profile found", "result": user_schema.dump(auth_info.user)}), 200


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": "user not found"}), 404

  if not check_ownership_or_rank(user_id, auth_info, 'Council'):
    return jsonify({"message": "can only update personal profile unless council+ rank"}), 403

  put_data = request.form if request.form else request.json

  if 'password' in put_data:
    put_data['password'] = generate_password_hash(put_data['password']).decode('utf8')

  if 'force_rank' in put_data and auth_info.user.force_rank != 'Grand Master':
    return jsonify({"message": "only grand masters have permissions to change force ranks"}), 403

  populate_object(user_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update user"}), 400

  return jsonify({"message": "user updated", "result": user_schema.dump(user_query)}), 200


@requires_min_rank('Grand Master')
def delete_user(user_id, auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": "user not found"}), 404

  try:
    db.session.delete(user_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete user"}), 400

  return jsonify({"message": "user removed from the force"}), 200
