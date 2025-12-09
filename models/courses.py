import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Courses(db.Model):
  __tablename__ = 'Courses'

  course_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Masters.master_id'), nullable=False)
  course_name = db.Column(db.String(), nullable=False, unique=True)
  difficulty = db.Column(db.String(), nullable=False)
  duration_weeks = db.Column(db.Integer(), nullable=False)
  max_students = db.Column(db.Integer(), default=20)

  instructor = db.relationship("Masters", back_populates="courses")
  enrollments = db.relationship("PadawanCourses", back_populates="course", cascade="all, delete-orphan")

  def __init__(self, instructor_id, course_name, difficulty, duration_weeks, max_students=20):
    self.instructor_id = instructor_id
    self.course_name = course_name
    self.difficulty = difficulty
    self.duration_weeks = duration_weeks
    self.max_students = max_students

  def new_course_obj():
    return Courses('', '', '', 0, 20)

class CoursesSchema(ma.Schema):
  class Meta:
      fields = ['course_id', 'instructor_id', 'course_name', 'difficulty', 'duration_weeks', 'max_students', 'instructor', 'enrollments']

  course_id = ma.fields.UUID()
  instructor_id = ma.fields.UUID(required=True)
  course_name = ma.fields.String(required=True)
  difficulty = ma.fields.String(required=True)
  duration_weeks = ma.fields.Integer(required=True)
  max_students = ma.fields.Integer()

  instructor = ma.fields.Nested("MastersSchema", exclude=['courses', 'padawans'])
  enrollments = ma.fields.Nested("PadawanCoursesSchema", many=True, exclude=['course'])


course_schema = CoursesSchema()
courses_schema = CoursesSchema(many=True)