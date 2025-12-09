from flask import jsonify, request

from db import db
from models.padawan_courses import PadawanCourses, padawan_course_schema
from models.padawans import Padawans
from models.courses import Courses
from util.reflection import populate_object
from lib.authenticate import requires_min_rank


@requires_min_rank('Master')
def add_enrollment(auth_info):
  post_data = request.form if request.form else request.json

  required_fields = ['padawan_id', 'course_id']
  for field in required_fields:
    if not post_data.get(field):
      return jsonify({"message": f"{field} is required"}), 400

  padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == post_data['padawan_id']).first()
  if not padawan_query:
    return jsonify({"message": "Padawan not found"}), 404

  course_query = db.session.query(Courses).filter(Courses.course_id == post_data['course_id']).first()
  if not course_query:
    return jsonify({"message": "Course not found"}), 404

  existing_enrollment = db.session.query(PadawanCourses).filter(PadawanCourses.padawan_id == post_data['padawan_id'], PadawanCourses.course_id == post_data['course_id']).first()

  if existing_enrollment:
    return jsonify({"message": "Padawan already enrolled in this course"}), 400

  new_enrollment = PadawanCourses.new_padawan_course_obj()
  populate_object(new_enrollment, post_data)

  try:
    db.session.add(new_enrollment)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "Unable to enroll padawan"}), 400

  return jsonify({"message": "Padawan enrolled", "result": padawan_course_schema.dump(new_enrollment)}), 201


@requires_min_rank('Master')
def delete_enrollment(padawan_id, course_id, auth_info):
  enrollment_query = db.session.query(PadawanCourses).filter(PadawanCourses.padawan_id == padawan_id, PadawanCourses.course_id == course_id).first()

  if not enrollment_query:
    return jsonify({"message": "Enrollment not found"}), 404

  try:
    db.session.delete(enrollment_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "Unable to remove enrollment"}), 400

  return jsonify({"message": "Padawan removed from course"}), 200