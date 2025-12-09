import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Lightsabers(db.Model):
  __tablename__ = 'Lightsabers'

  saber_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
  crystal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Crystals.crystal_id'), nullable=False)
  saber_name = db.Column(db.String(), nullable=False, unique=True)
  hilt_material = db.Column(db.String(), nullable=False)
  blade_color = db.Column(db.String(), nullable=False)
  is_completed = db.Column(db.Boolean(), default=False)

  owner = db.relationship("Users", back_populates="lightsabers")
  crystal = db.relationship("Crystals", back_populates="lightsabers")

  def __init__(self, owner_id, crystal_id, saber_name, hilt_material, blade_color, is_completed=False):
    self.owner_id = owner_id
    self.crystal_id = crystal_id
    self.saber_name = saber_name
    self.hilt_material = hilt_material
    self.blade_color = blade_color
    self.is_completed = is_completed

  def new_lightsaber_obj():
    return Lightsabers('', '', '', '', '', False)

class LightsabersSchema(ma.Schema):
  class Meta:
    fields = ['saber_id', 'owner_id', 'crystal_id', 'saber_name', 'hilt_material', 'blade_color', 'is_completed', 'owner', 'crystal']

  saber_id = ma.fields.UUID()
  owner_id = ma.fields.UUID(required=True)
  crystal_id = ma.fields.UUID(required=True)
  saber_name = ma.fields.String(required=True)
  hilt_material = ma.fields.String(required=True)
  blade_color = ma.fields.String(required=True)
  is_completed = ma.fields.Boolean()

  owner = ma.fields.Nested("UsersSchema", only=['user_id', 'username', 'force_rank'])
  crystal = ma.fields.Nested("CrystalsSchema", exclude=['lightsabers'])


lightsaber_schema = LightsabersSchema()
lightsabers_schema = LightsabersSchema(many=True)