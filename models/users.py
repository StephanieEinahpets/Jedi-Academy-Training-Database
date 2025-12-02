import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db


class Users(db.Model):
  __tablename__ = 'Users'

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Temples.temple_id'))
  username = db.Column(db.String(), nullable=False, unique=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  force_rank = db.Column(db.String(), nullable=False, default='Youngling')
  midi_count = db.Column(db.Integer(), default=2500)
  is_active = db.Column(db.Boolean(), default=True)
  joined_date = db.Column(db.DateTime(), default=datetime.utcnow)

  temple = db.relationship("Temples", back_populates="users")
  auth_tokens = db.relationship("AuthTokens", back_populates="user", cascade="all, delete-orphan")
  padawan = db.relationship("Padawans", back_populates="user", uselist=False, cascade="all, delete-orphan")
  masters = db.relationship("Masters", back_populates="user", cascade="all, delete-orphan")
  lightsabers = db.relationship("Lightsabers", back_populates="owner", cascade="all, delete-orphan")

  def __init__(self, temple_id, username, email, password, force_rank='Youngling', midi_count=2500, is_active=True):
    self.temple_id = temple_id
    self.username = username
    self.email = email
    self.password = password
    self.force_rank = force_rank
    self.midi_count = midi_count
    self.is_active = is_active

  def new_user_obj():
    return Users('', '', '', '', 'Youngling', 2500, True)


class UsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id', 'temple_id', 'username', 'email', 'force_rank', 'midi_count', 'is_active', 'joined_date', 'temple', 'padawan', 'masters']

  user_id = ma.fields.UUID()
  temple_id = ma.fields.UUID(allow_none=True)
  username = ma.fields.String(required=True)
  email = ma.fields.String(required=True)
  force_rank = ma.fields.String(required=True)
  midi_count = ma.fields.Integer()
  is_active = ma.fields.Boolean()
  joined_date = ma.fields.DateTime()

  temple = ma.fields.Nested("TemplesSchema", exclude=['users'])
  padawan = ma.fields.Nested("PadawansSchema", exclude=['user'])
  masters = ma.fields.Nested("MastersSchema", many=True, exclude=['user'])


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
