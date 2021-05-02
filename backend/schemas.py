from marshmallow import Schema, fields, pre_load, post_dump, validate

# dump_only = read only fields
# load_only = write only fields

class UserSchema(Schema):
  id = fields.UUID(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True, validate=validate.Email(error="Not a valid email address"))
  password = fields.Str(required=True, load_only=True, validate=[validate.Length(min=6)])

class CourseSchema(Schema):
  id = fields.UUID(dump_only=True)
  name = fields.Str(required=True)
  description = fields.Str()
  due = fields.Date(required=True)
  status = fields.Str(dump_only=True)
  syllabus = fields.List(fields.Dict())
  owner = fields.Nested(
    UserSchema(exclude=['password']),
    dump_only=True,
    required=True
  )
  class Meta:
    strict = True

class TopicSchema(Schema):
  id = fields.UUID(dump_only=True)
  name = fields.Str(required=True)
class ResourceSchema(Schema):
  id = fields.UUID(dump_only=True)
  name = fields.Str(required=True)
  url = fields.Url(required=True)
  votes = fields.Int(dump_only=True)
  # topics = fields.List(fields.Nested(TopicSchema))