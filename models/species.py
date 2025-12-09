import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Species(db.Model):
  __tablename__ = 'Species'

  species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  species_name = db.Column(db.String(), nullable=False, unique=True)
  homeworld = db.Column(db.String(), nullable=False)
  force_sensitive = db.Column(db.Boolean(), default=True)
  avg_lifespan = db.Column(db.Integer(), nullable=False)

  padawans = db.relationship("Padawans", back_populates="species")

  def __init__(self, species_name, homeworld, force_sensitive=True, avg_lifespan=100):
    self.species_name = species_name
    self.homeworld = homeworld
    self.force_sensitive = force_sensitive
    self.avg_lifespan = avg_lifespan

  def new_species_obj():
    return Species('', '', True, 100)

class SpeciesSchema(ma.Schema):
  class Meta:
    fields = ['species_id', 'species_name', 'homeworld', 'force_sensitive', 'avg_lifespan', 'padawans']

  species_id = ma.fields.UUID()
  species_name = ma.fields.String(required=True)
  homeworld = ma.fields.String(required=True)
  force_sensitive = ma.fields.Boolean()
  avg_lifespan = ma.fields.Integer(required=True)

  padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['species'])


species_schema = SpeciesSchema()
species_list_schema = SpeciesSchema(many=True)