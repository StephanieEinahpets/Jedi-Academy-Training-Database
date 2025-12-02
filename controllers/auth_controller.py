from flask import jsonify, request
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from models.auth_tokens import AuthTokens, auth_token_schema
from models.users import Users
from lib.authenticate import authenticate_return_auth


RANK_TOKEN_EXPIRATION = {
  'Grand Master': 72,
  'Council': 48,
  'Master': 24,
  'Knight': 12,
  'Padawan': 8,
  'Youngling': 4
}


def auth_token_add():
  post_data = request.form if request.form else request.json
  email = post_data.get('email')
  password = post_data.get('password')

  if not email or not password:
    return jsonify({"message": "email and password required"}), 401

  user_query = db.session.query(Users).filter(Users.email == email).first()

  if not user_query:
    return jsonify({"message": "invalid credentials"}), 401

  if not user_query.is_active:
    return jsonify({"message": "account deactivated - contact the jedi council"}), 401

  is_password_valid = check_password_hash(user_query.password, password)

  if not is_password_valid:
    return jsonify({"message": "invalid credentials"}), 401

  hours = RANK_TOKEN_EXPIRATION.get(user_query.force_rank, 4)
  expiration_datetime = datetime.now() + timedelta(hours=hours)

  existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_query.user_id).all()
  for token in existing_tokens:
    if token.expiration_date < datetime.now():
      db.session.delete(token)

  new_token = AuthTokens(user_id=user_query.user_id, expiration_date=expiration_datetime)

  try:
    db.session.add(new_token)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create auth token"}), 400

  return jsonify({"message": "may the force be with you", "auth_info": auth_token_schema.dump(new_token)}), 201


@authenticate_return_auth
def auth_token_delete(auth_info):
  try:
    db.session.delete(auth_info)
    db.session.commit()
    return jsonify({"message": "force connection severed - logout successful"}), 200
  except:
    db.session.rollback()
    return jsonify({"message": "error logging out"}), 400
