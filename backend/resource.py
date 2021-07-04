from rich import print
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from marshmallow import ValidationError

from models import Resource, ResourceTopic, Topic
from schemas import ResourceSchema, TopicDumpSchema, TopicSchema, ResourceDumpSchema, ResourceLoadSchema

resource = Blueprint('resource', __name__)

@resource.route('/create', methods=['POST'])
@jwt_required()
def create_resource():
  json_input = request.get_json()
  # validate
  try:
    data = ResourceLoadSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  print(data)
  # create the course
  resource = Resource.create(**data)
  return ResourceDumpSchema().dump(resource)

@resource.route('/<id>', methods=['GET'])
def get_resource(id):
  try:
    resource = Resource.get(Resource.id == id)
  except Resource.DoesNotExist:
    return {'errors': ['Resource not found']}, 404
  return ResourceDumpSchema().dump(resource)

def vote_resource(id, vote):
  resource = Resource.get(Resource.id == id)
  resource.votes = resource.votes + vote
  resource.save()
  return resource

@resource.route('/<id>/upvote', methods=['POST'])
def upvote_resource(id):
  resource = vote_resource(id, 1)
  return ResourceDumpSchema().dump(resource)

@resource.route('/<id>/downvote', methods=['POST'])
def downvote_resource(id):
  resource = vote_resource(id, -1)
  return ResourceDumpSchema().dump(resource)

@resource.route('/<id>/broken', methods=['POST'])
def mark_broken_resource(id):
  resource = Resource.get(Resource.id == id)
  resource.isBroken += 1
  resource.save()
  return jsonify({'success': True})

@resource.route('/', methods=['GET'])
def get_all_resources():
  searchQuery = request.args.get('search')
  topics = request.args.get('topics')

  # TODO(TOM): search and topics similtaniously
  if searchQuery:
    resources = Resource.select().where(
      Resource.name.contains(searchQuery)
    ).order_by(Resource.votes.desc()).limit(100)
  elif topics:
    topics = topics.split(',')
    resources = (Resource.select()
                        .join(ResourceTopic)
                        .join(Topic)
                        .where(Topic.name.in_(topics))
                        .order_by(Resource.votes.desc())
                )
  else:
    resources = Resource.select().order_by(Resource.votes.desc()).limit(100)
  return {'resources': ResourceDumpSchema().dump(resources, many=True)}

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

@resource.route('/topics', methods=['GET'])
def get_all_topics():
  topics = Topic.select()
  return {"topics": TopicDumpSchema().dump(topics, many=True)}

@resource.route('/topic', methods=['POST'])
def create_topic():
  json_input = request.get_json()
  try:
    data = TopicSchema().load(json_input)
  except ValidationError as err:
    return {'errors': err.messages}, 422
  # create the topic
  topic = Topic.create(**data)
  return TopicDumpSchema().dump(topic)