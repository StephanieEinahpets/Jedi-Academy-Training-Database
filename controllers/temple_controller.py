from flask import jsonify, request

from db import db
from models.temples import Temples, temple_schema, temples_schema
from util.reflection import populate_object
from lib.authenticate import requires_min_rank


@requires_min_rank('Grand Master')
def add_temple(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['temple_name', 'planet']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  new_temple = Temples.new_temple_obj()
  populate_object(new_temple, post_data)
  try:
    db.session.add(new_temple)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create temple -  name may already exist"}), 400

  return jsonify({"message": "temple established", "result": temple_schema.dump(new_temple)}), 201


def get_temple_by_id(temple_id):
  temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

  if not temple_query:
    return jsonify({"message": "temple not found"}), 404

  return jsonify({"message": "temple found", "result": temple_schema.dump(temple_query)}), 200


@requires_min_rank('Grand Master')
def update_temple(temple_id, auth_info):
  temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

  if not temple_query:
    return jsonify({"message": "temple not found"}), 404

  put_data = request.form if request.form else request.json
  populate_object(temple_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update temple"}), 400

  return jsonify({"message": "temple updated", "result": temple_schema.dump(temple_query)}), 200


@requires_min_rank('Grand Master')
def delete_temple(temple_id, auth_info):
  temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

  if not temple_query:
    return jsonify({"message": "temple not found"}), 404

  temple_query.is_active = False

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to deactivate temple"}), 400

  return jsonify({"message": "temple deactivated"}), 200