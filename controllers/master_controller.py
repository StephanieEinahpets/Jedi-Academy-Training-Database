from flask import jsonify, request

from db import db
from models.masters import Masters, master_schema, masters_schema
from models.users import Users
from util.reflection import populate_object
from lib.authenticate import requires_min_rank, authenticate_return_auth, check_ownership_or_rank


@requires_min_rank('Council')
def add_master(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['user_id', 'master_name', 'specialization']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  user_query = db.session.query(Users).filter(Users.user_id == post_data['user_id']).first()
  if not user_query:
    return jsonify({"message": "user not found"}), 404

  user_query.force_rank = 'Master'

  new_master = Masters(
    user_id=post_data['user_id'],
    master_name=post_data['master_name'],
    specialization=post_data['specialization'],
    years_training=post_data.get('years_training', 0),
    max_padawans=post_data.get('max_padawans', 3)
  )

  try:
    db.session.add(new_master)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create master"}), 400

  return jsonify({"message": "master created", "result": master_schema.dump(new_master)}), 201


@requires_min_rank('Padawan')
def get_all_masters(auth_info):
  masters_query = db.session.query(Masters).all()
  return jsonify({"message": "masters found", "results": masters_schema.dump(masters_query)}), 200


@authenticate_return_auth
def update_master(master_id, auth_info):
  master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

  if not master_query:
    return jsonify({"message": "master not found"}), 404

  if not check_ownership_or_rank(master_query.user_id, auth_info, 'Council'):
    return jsonify({"message": "may only update personal profile if council+ rank"}), 403

  put_data = request.form if request.form else request.json
  populate_object(master_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update master"}), 400

  return jsonify({"message": "master updated", "result": master_schema.dump(master_query)}), 200


@requires_min_rank('Grand Master')
def delete_master(master_id, auth_info):
  master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

  if not master_query:
    return jsonify({"message": "master not found"}), 404

  user_query = db.session.query(Users).filter(Users.user_id == master_query.user_id).first()
  user_query.force_rank = 'Knight'

  try:
    db.session.delete(master_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete master"}), 400

  return jsonify({"message": "master status removed"}), 200