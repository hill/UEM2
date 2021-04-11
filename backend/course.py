from rich import print
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from playhouse.shortcuts import model_to_dict
from marshmallow import ValidationError

from models import Course
from schemas import CourseSchema

course = Blueprint('course', __name__)

@course.route('/create', methods=['POST'])
@jwt_required()
def create_course():
  json_input = request.get_json()
  user_id = get_jwt_identity()
  
  # validate
  try:
    data = CourseSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  
  # create the course
  c = Course.create(**data, owner_id=user_id)
  return CourseSchema().dump(c)

@course.route('/<id>', methods=['GET'])
def get_course(id):
  try:
    course = Course.get(Course.id == id)
  except Course.DoesNotExist:
    return {'errors': ['Course not found']}, 404
  return CourseSchema().dump(course)

@course.route('/', methods=['GET'])
@jwt_required()
def get_user_courses():
  courses = Course.select().where(Course.owner_id == get_jwt_identity())
  return {'courses': CourseSchema().dump(courses, many=True)}

@course.route('/<id>', methods=['PUT'])
@jwt_required()
def update_course(id):
  course = Course.get(Course.id == id)
  if not course:
    return {'errors': ['Course not found']}, 404
  if not course.is_owned_by(get_jwt_identity()):
    return {'errors': ['Unauthorized']}, 405
  
  json_input = request.json
  try:
    data = CourseSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  
  query = Course.update(**data).where(Course.id == id)
  query.execute()
  return {'message': 'success'}


@course.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
  course = Course.get(Course.id == id)
  if not course:
    return {'errors': ['Course not found']}, 404
  if not course.is_owned_by(get_jwt_identity()):
    return {'errors': ['Unauthorized']}, 405
  
  Course.delete_by_id(id)
  return {'message': 'success'}