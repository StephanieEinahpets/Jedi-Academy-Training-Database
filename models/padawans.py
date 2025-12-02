import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class Padawans(db.Model):
  __tablename__ = 'Padawans'

  padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  master_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Masters.master_id'))
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
  species_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Species.species_id'), nullable=False)
  padawan_name = db.Column(db.String(), nullable=False, unique=True)
  age = db.Column(db.Integer(), nullable=False)
  training_level = db.Column(db.Integer(), default=1)
  graduation_date = db.Column(db.DateTime())

  master = db.relationship("Masters", back_populates="padawans", foreign_keys=[master_id])
  user = db.relationship("Users", back_populates="padawan")
  species = db.relationship("Species", back_populates="padawans")
  courses = db.relationship("PadawanCourses", back_populates="padawan", cascade="all, delete-orphan")

  def __init__(self, user_id, species_id, padawan_name, age, master_id=None, training_level=1):
    self.master_id = master_id
    self.user_id = user_id
    self.species_id = species_id
    self.padawan_name = padawan_name
    self.age = age
    self.training_level = training_level


class PadawansSchema(ma.Schema):
  class Meta:
    fields = ['padawan_id', 'master_id', 'user_id', 'species_id', 'padawan_name', 'age', 'training_level', 'graduation_date', 'master', 'user', 'species', 'courses']

  padawan_id = ma.fields.UUID()
  master_id = ma.fields.UUID(allow_none=True)
  user_id = ma.fields.UUID(required=True)
  species_id = ma.fields.UUID(required=True)
  padawan_name = ma.fields.String(required=True)
  age = ma.fields.Integer(required=True)
  training_level = ma.fields.Integer()
  graduation_date = ma.fields.DateTime(allow_none=True)

  master = ma.fields.Nested("MastersSchema", exclude=['padawans'])
  user = ma.fields.Nested("UsersSchema", only=['user_id', 'username', 'email', 'force_rank'])
  species = ma.fields.Nested("SpeciesSchema", exclude=['padawans'])
  courses = ma.fields.Nested("PadawanCoursesSchema", many=True, exclude=['padawan'])


padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)