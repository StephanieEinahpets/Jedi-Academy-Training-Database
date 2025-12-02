from flask import Flask
import os

from db import *
from util.blueprints import register_blueprint
from seed_data import seed_database

flask_host = os.environ.get('FLASK_HOST')
flask_port = os.environ.get('FLASK_PORT')

database_scheme = os.environ.get('DATABASE_SCHEME')
database_user = os.environ.get('DATABASE_USER')
database_address = os.environ.get('DATABASE_ADDRESS')
database_port = os.environ.get('DATABASE_PORT')
database_name = os.environ.get('DATABASE_NAME')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False


init_db(app, db)

register_blueprint(app)

def create_tables():
  with app.app_context():
    print("Creating Tables...")
    db.create_all()
    print("Tables Created Successfully")

if __name__ == '__main__':
  create_tables()
  seed_database(app)
  app.run(host=flask_host, port=flask_port)