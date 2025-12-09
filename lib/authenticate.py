import functools
from flask import jsonify, request
from datetime import datetime
from uuid import UUID

from db import db
from models.auth_tokens import AuthTokens


FORCE_RANKS = {
  'Grand Master': 1,
  'Council': 2,
  'Master': 3,
  'Knight': 4,
  'Padawan': 5,
  'Youngling': 6
}


def validate_uuid4(uuid_string):
  try:
    UUID(uuid_string, version=4)
    return True
  except:
    return False


def validate_token():
  auth_token = request.headers.get('Authorization')

  if not auth_token or not validate_uuid4(auth_token):
    return False

  existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

  if existing_token:
    if existing_token.expiration_date > datetime.now():
      return existing_token

  return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def authenticate(func):
  @functools.wraps(func)
  def wrapper_authenticate(*args, **kwargs):
    auth_info = validate_token()
    return (
      func(*args, **kwargs) if auth_info else fail_response()
    )

  return wrapper_authenticate


def authenticate_return_auth(func):
  @functools.wraps(func)
  def wrapper_authenticate(*args, **kwargs):
    auth_info = validate_token()
    kwargs['auth_info'] = auth_info

    return (
      func(*args, **kwargs) if auth_info else fail_response()
    )

  return wrapper_authenticate



def forbidden_response(message="insufficient force rank for this action"):
  return jsonify({"message": message}), 403


def requires_force_rank(*allowed_ranks):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      auth_info = validate_token()
      
      if not auth_info:
        return fail_response()
      
      user_rank = auth_info.user.force_rank
      
      if user_rank not in allowed_ranks:
        return forbidden_response(
          f"action requires {' or '.join(allowed_ranks)} rank"
        )
      
      kwargs['auth_info'] = auth_info
      return func(*args, **kwargs)
    return wrapper
  return decorator


def requires_min_rank(min_rank):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      auth_info = validate_token()
      
      if not auth_info:
        return fail_response()
      
      user_rank = auth_info.user.force_rank
      
      if FORCE_RANKS.get(user_rank, 999) > FORCE_RANKS.get(min_rank, 0):
        return forbidden_response(
          f"action requires minimum rank of {min_rank}"
        )
      
      kwargs['auth_info'] = auth_info
      return func(*args, **kwargs)
    return wrapper
  return decorator


def check_ownership_or_rank(user_id, auth_info, min_rank='Council'):
  is_owner = str(auth_info.user.user_id) == str(user_id)
  has_rank = FORCE_RANKS.get(auth_info.user.force_rank, 999) <= FORCE_RANKS.get(min_rank, 0)
  
  return is_owner or has_rank




# import functools
# from flask import jsonify, request
# from datetime import datetime
# from uuid import UUID

# from db import db
# from models.auth_tokens import AuthTokens


# FORCE_RANKS = {
#   'Grand Master': 1,
#   'Council': 2,
#   'Master': 3,
#   'Knight': 4,
#   'Padawan': 5,
#   'Youngling': 6
# }


# def validate_uuid4(uuid_string):
#   try:
#     UUID(uuid_string, version=4)
#     return True
#   except:
#     return False


# def validate_token():
#   auth_token = request.headers.get('Authorization')

#   if not auth_token or not validate_uuid4(auth_token):
#     return False

#   existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

#   if existing_token:
#     if existing_token.expiration_date > datetime.now():
#       return existing_token

#   return False


# def fail_response(message="authentication required"):
#   return jsonify({"message": message}), 401


# def forbidden_response(message="insufficient force rank for this action"):
#   return jsonify({"message": message}), 403


# def authenticate(func):
#   @functools.wraps(func)
#   def wrapper_authenticate(*args, **kwargs):
#     auth_info = validate_token()
#     return func(*args, **kwargs) if auth_info else fail_response()
#   return wrapper_authenticate


# def authenticate_return_auth(func):
#   @functools.wraps(func)
#   def wrapper_authenticate(*args, **kwargs):
#     auth_info = validate_token()
#     kwargs['auth_info'] = auth_info
#     return func(*args, **kwargs) if auth_info else fail_response()
#   return wrapper_authenticate


# def requires_force_rank(*allowed_ranks):
#   def decorator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#       auth_info = validate_token()
      
#       if not auth_info:
#         return fail_response()
      
#       user_rank = auth_info.user.force_rank
      
#       if user_rank not in allowed_ranks:
#         return forbidden_response(
#           f"action requires {' or '.join(allowed_ranks)} rank"
#         )
      
#       kwargs['auth_info'] = auth_info
#       return func(*args, **kwargs)
#     return wrapper
#   return decorator


# def requires_min_rank(min_rank):
#   def decorator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#       auth_info = validate_token()
      
#       if not auth_info:
#         return fail_response()
      
#       user_rank = auth_info.user.force_rank
      
#       if FORCE_RANKS.get(user_rank, 999) > FORCE_RANKS.get(min_rank, 0):
#         return forbidden_response(
#           f"action requires minimum rank of {min_rank}"
#         )
      
#       kwargs['auth_info'] = auth_info
#       return func(*args, **kwargs)
#     return wrapper
#   return decorator


# def check_ownership_or_rank(user_id, auth_info, min_rank='Council'):
#   is_owner = str(auth_info.user.user_id) == str(user_id)
#   has_rank = FORCE_RANKS.get(auth_info.user.force_rank, 999) <= FORCE_RANKS.get(min_rank, 0)
  
#   return is_owner or has_rank