from flask import Blueprint
import controllers

auth = Blueprint('auth', __name__)


@auth.route('/user/auth', methods=['POST'])
def auth_token_add_route():
  return controllers.auth_token_add()

@auth.route('/logout', methods=['DELETE'])
def auth_token_delete_route():
  return controllers.auth_token_delete()