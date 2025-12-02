from flask import Blueprint

import controllers

search = Blueprint('search', __name__)


@search.route('/users/search', methods=['GET'])
def users_get_by_search_route():
  return controllers.users_get_by_search()