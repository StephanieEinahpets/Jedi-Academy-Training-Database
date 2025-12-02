from flask import jsonify, request

from db import db
from models.padawans import Padawans, padawan_schema, padawans_schema
from models.users import Users
from models.species import Species
from models.masters import Masters
from util.reflection import populate_object
from lib.authenticate import requires_min_rank, authenticate_return_auth
from datetime import datetime


@requires_min_rank('Master')
def add_padawan(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['user_id', 'species_id', 'padawan_name', 'age']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  user_query = db.session.query(Users).filter(Users.user_id == post_data['user_id']).first()
  if not user_query:
    return jsonify({"message": "user not found"}), 404

  species_query = db.session.query(Species).filter(Species.species_id == post_data['species_id']).first()
  if not species_query:
    return jsonify({"message": "species not found"}), 404

  master_id = post_data.get('master_id')
  if master_id:
    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()
    if not master_query:
      return jsonify({"message": "master not found"}), 404

  new_padawan = Padawans(
    user_id=post_data['user_id'],
    species_id=post_data['species_id'],
    padawan_name=post_data['padawan_name'],
    age=post_data['age'],
    master_id=master_id,
    training_level=post_data.get('training_level', 1)
  )

  try:
    db.session.add(new_padawan)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create padawan"}), 400

  return jsonify({"message": "padawan created", "result": padawan_schema.dump(new_padawan)}), 201


@requires_min_rank('Master')
def get_all_padawans(auth_info):
  temple_id = auth_info.user.temple_id
  padawans_query = db.session.query(Padawans).join(Users).filter(Users.temple_id == temple_id).all()
  return jsonify({"message": "padawans found", "results": padawans_schema.dump(padawans_query)}), 200


@authenticate_return_auth
def get_active_padawans(auth_info):
  padawans_query = db.session.query(Padawans).filter(Padawans.graduation_date == None).all()
  return jsonify({"message": "active padawans found", "results": padawans_schema.dump(padawans_query)}), 200


@authenticate_return_auth
def update_padawan(padawan_id, auth_info):
  padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

  if not padawan_query:
    return jsonify({"message": "padawan not found"}), 404

  is_master = padawan_query.master and str(padawan_query.master.user_id) == str(auth_info.user.user_id)
  is_council = auth_info.user.force_rank in ['Council', 'Grand Master']

  if not (is_master or is_council):
    return jsonify({"message": "must be master or council+ to update padawan"}), 403

  put_data = request.form if request.form else request.json
  populate_object(padawan_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update padawan"}), 400

  return jsonify({"message": "padawan updated", "result": padawan_schema.dump(padawan_query)}), 200


@requires_min_rank('Council')
def promote_padawan(padawan_id, auth_info):
  padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

  if not padawan_query:
    return jsonify({"message": "padawan not found"}), 404

  user_query = db.session.query(Users).filter(Users.user_id == padawan_query.user_id).first()
  user_query.force_rank = 'Knight'

  padawan_query.graduation_date = datetime.now()

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to promote padawan"}), 400

  return jsonify({"message": "padawan promoted", "result": padawan_schema.dump(padawan_query)}), 200


@requires_min_rank('Council')
def delete_padawan(padawan_id, auth_info):
  padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

  if not padawan_query:
    return jsonify({"message": "padawan not found"}), 404

  try:
    db.session.delete(padawan_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete padawan"}), 400

  return jsonify({"message": "padawan record removed"}), 200
