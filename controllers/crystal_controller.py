from flask import jsonify, request

from db import db
from models.crystals import Crystals, crystal_schema, crystals_schema
from lib.authenticate import requires_min_rank


@requires_min_rank('Master')
def add_crystal(auth_info):
  post_data = request.form if request.form else request.json
  required_fields = ['crystal_type', 'origin_planet', 'rarity_level']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  new_crystal = Crystals(
    crystal_type=post_data['crystal_type'],
    origin_planet=post_data['origin_planet'],
    rarity_level=post_data['rarity_level'],
    force_amplify=post_data.get('force_amplify', 1.0)
  )

  try:
    db.session.add(new_crystal)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to catalog crystal"}), 400

  return jsonify({"message": "crystal cataloged", "result": crystal_schema.dump(new_crystal)}), 201


@requires_min_rank('Master')
def get_crystals_by_rarity(rarity_level, auth_info):
  crystals_query = db.session.query(Crystals).filter(Crystals.rarity_level == rarity_level).all()

  if not crystals_query:
    return jsonify({"message": f"no crystals found with rarity {rarity_level}"}), 404

  return jsonify({"message": "crystals found", "results": crystals_schema.dump(crystals_query)}), 200

