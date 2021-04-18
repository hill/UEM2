from rich import print
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from marshmallow import ValidationError

from models import Resource, Topic
from schemas import ResourceSchema, TopicSchema

resource = Blueprint('resource', __name__)

@resource.route('/create', methods=['POST'])
@jwt_required()
def create_resource():
  json_input = request.get_json()
  
  # validate
  try:
    data = ResourceSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  
  # create the course
  resource = Resource.create(**data)
  return ResourceSchema().dump(resource)

@resource.route('/<id>', methods=['GET'])
def get_resource(id):
  try:
    resource = Resource.get(Course.id == id)
  except Resource.DoesNotExist:
    return {'errors': ['Course not found']}, 404
  return ResourceSchema().dump(resource)

@resource.route('/', methods=['GET'])
@jwt_required()
def get_all_resources():
  resources = Resource.select().limit(100)
  return {'courses': ResourceSchema().dump(resources, many=True)}

@resource.route('/<id>', methods=['PUT'])
@jwt_required()
def update_resource(id):
  resource = Resource.get(Resource.id == id)
  if not resource:
    return {'errors': ['Resource not found']}, 404
  # if not resource.is_owned_by(get_jwt_identity()):
  #   return {'errors': ['Unauthorized']}, 405
  
  json_input = request.json
  try:
    data = ResourceSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  
  query = Resource.update(**data).where(Resource.id == id)
  query.execute()
  return {'message': 'success'}


@resource.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_resource(id):
  resource = Resource.get(Resource.id == id)
  if not resource:
    return {'errors': ['Resource not found']}, 404
  # if not resource.is_owned_by(get_jwt_identity()):
  #   return {'errors': ['Unauthorized']}, 405
  
  Resource.delete_by_id(id)
  return {'message': 'success'}