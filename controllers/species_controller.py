from flask import jsonify, request

from db import db
from models.species import Species, species_schema, species_list_schema
from util.reflection import populate_object
from lib.authenticate import requires_min_rank


@requires_min_rank('Master')
def add_species(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['species_name', 'homeworld', 'avg_lifespan']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  new_species = Species.new_species_obj()
  populate_object(new_species, post_data)

  try:
    db.session.add(new_species)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create species"}), 400

  return jsonify({"message": "species documented", "result": species_schema.dump(new_species)}), 201


def get_species_by_id(species_id):
  species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

  if not species_query:
    return jsonify({"message": "species not found"}), 404

  return jsonify({"message": "species found", "result": species_schema.dump(species_query)}), 200
