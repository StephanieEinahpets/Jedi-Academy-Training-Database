from flask import jsonify, request

from db import db
from models.lightsabers import Lightsabers, lightsaber_schema, lightsabers_schema
from models.crystals import Crystals
from models.users import Users
from util.reflection import populate_object
from lib.authenticate import requires_min_rank, authenticate_return_auth, check_ownership_or_rank


@requires_min_rank('Padawan')
def add_lightsaber(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['owner_id', 'crystal_id', 'saber_name', 'hilt_material', 'blade_color']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  owner_query = db.session.query(Users).filter(Users.user_id == post_data['owner_id']).first()
  if not owner_query:
    return jsonify({"message": "owner not found"}), 404

  crystal_query = db.session.query(Crystals).filter(Crystals.crystal_id == post_data['crystal_id']).first()
  if not crystal_query:
    return jsonify({"message": "crystal not found"}), 404

  new_lightsaber = Lightsabers.new_lightsaber_obj()
  populate_object(new_lightsaber, post_data)

  try:
    db.session.add(new_lightsaber)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create lightsaber"}), 400

  return jsonify({"message": "lightsaber construction complete", "result": lightsaber_schema.dump(new_lightsaber)}), 201


def get_lightsaber_by_owner(owner_id):
  lightsabers_query = db.session.query(Lightsabers).filter(Lightsabers.owner_id == owner_id).all()

  if not lightsabers_query:
    return jsonify({"message": "no lightsabers found for this owner"}), 404

  return jsonify({"message": "lightsabers found", "results": lightsabers_schema.dump(lightsabers_query)}), 200


@authenticate_return_auth
def update_lightsaber(saber_id, auth_info):
  lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()

  if not lightsaber_query:
    return jsonify({"message": "lightsaber not found"}), 404

  if str(lightsaber_query.owner_id) != str(auth_info.user.user_id):
    return jsonify({"message": "only the owner may alter this lightsaber"}), 403

  put_data = request.form if request.form else request.json
  populate_object(lightsaber_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to customize lightsaber"}), 400

  return jsonify({"message": "lightsaber customized", "result": lightsaber_schema.dump(lightsaber_query)}), 200


@authenticate_return_auth
def delete_lightsaber(saber_id, auth_info):
  lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()

  if not lightsaber_query:
    return jsonify({"message": "lightsaber not found"}), 404

  if not check_ownership_or_rank(lightsaber_query.owner_id, auth_info, 'Council'):
    return jsonify({"message": "only owner or council+ can destroy this lightsaber"}), 403

  try:
    db.session.delete(lightsaber_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to destroy lightsaber"}), 400

  return jsonify({"message": "lightsaber destroyed"}), 200

