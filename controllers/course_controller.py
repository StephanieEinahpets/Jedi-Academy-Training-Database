from flask import jsonify, request

from db import db
from models.courses import Courses, course_schema, courses_schema
from models.masters import Masters
from util.reflection import populate_object
from lib.authenticate import requires_min_rank, authenticate_return_auth


@requires_min_rank('Master')
def add_course(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['instructor_id', 'course_name', 'difficulty', 'duration_weeks']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  instructor_query = db.session.query(Masters).filter(Masters.master_id == post_data['instructor_id']).first()
  if not instructor_query:
    return jsonify({"message": "Instructor not found"}), 404

  new_course = Courses.new_course_obj()
  populate_object(new_course, post_data)

  try:
    db.session.add(new_course)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "Unable to create course. Name may already exist"}), 400

  return jsonify({"message": "Course created", "result": course_schema.dump(new_course)}), 201


def get_courses_by_difficulty(difficulty_level):
  courses_query = db.session.query(Courses).filter(Courses.difficulty == difficulty_level).all()

  if not courses_query:
    return jsonify({"message": f"No courses found with difficulty: {difficulty_level}"}), 404

  return jsonify({"message": "Courses found", "results": courses_schema.dump(courses_query)}), 200


@authenticate_return_auth
def update_course(course_id, auth_info):
  course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

  if not course_query:
    return jsonify({"message": "Course not found"}), 404

  is_instructor = str(course_query.instructor.user_id) == str(auth_info.user.user_id)
  is_council = auth_info.user.force_rank in ['Council', 'Grand Master']

  if not (is_instructor or is_council):
    return jsonify({"message": "Only instructor or Council+ can update course"}), 403

  put_data = request.form if request.form else request.json
  populate_object(course_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "Unable to update course"}), 400

  return jsonify({"message": "Course updated", "result": course_schema.dump(course_query)}), 200


@authenticate_return_auth
def delete_course(course_id, auth_info):
  course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

  if not course_query:
    return jsonify({"message": "Course not found"}), 404

  is_instructor = str(course_query.instructor.user_id) == str(auth_info.user.user_id)
  is_council = auth_info.user.force_rank in ['Council', 'Grand Master']

  if not (is_instructor or is_council):
    return jsonify({"message": "Only instructor or Council+ can cancel course"}), 403

  try:
    db.session.delete(course_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "Unable to delete course"}), 400

  return jsonify({"message": "Course canceled"}), 200

