from flask import Blueprint
import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user_route():
  return controllers.add_user()


@users.route('/users', methods=['GET'])
def get_all_users_route():
  return controllers.get_all_users()


@users.route('/user/profile', methods=['GET'])
def get_user_profile_route():
  return controllers.get_user_profile()


@users.route('/user/<user_id>', methods=['PUT'])
def update_user_by_id_route(user_id):
  return controllers.update_user_by_id(user_id)


@users.route('/user/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
  return controllers.delete_user(user_id)
