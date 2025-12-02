import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Masters(db.Model):
  __tablename__ = 'Masters'

  master_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
  master_name = db.Column(db.String(), nullable=False, unique=True)
  specialization = db.Column(db.String(), nullable=False)
  years_training = db.Column(db.Integer(), default=0)
  max_padawans = db.Column(db.Integer(), default=3)

  user = db.relationship("Users", back_populates="masters")
  padawans = db.relationship("Padawans", back_populates="master", foreign_keys="Padawans.master_id")
  courses = db.relationship("Courses", back_populates="instructor")

  def __init__(self, user_id, master_name, specialization, years_training=0, max_padawans=3):
    self.user_id = user_id
    self.master_name = master_name
    self.specialization = specialization
    self.years_training = years_training
    self.max_padawans = max_padawans


class MastersSchema(ma.Schema):
  class Meta:
    fields = ['master_id', 'user_id', 'master_name', 'specialization', 'years_training', 'max_padawans', 'user', 'padawans']

  master_id = ma.fields.UUID()
  user_id = ma.fields.UUID(required=True)
  master_name = ma.fields.String(required=True)
  specialization = ma.fields.String(required=True)
  years_training = ma.fields.Integer()
  max_padawans = ma.fields.Integer()

  user = ma.fields.Nested("UsersSchema", only=['user_id', 'username', 'email', 'force_rank'])
  padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['master'])


master_schema = MastersSchema()
masters_schema = MastersSchema(many=True)