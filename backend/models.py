import uuid
from peewee import *
from playhouse.sqlite_ext import JSONField
db = SqliteDatabase('newDb.db')

class BaseModel(Model):
  id = CharField(primary_key=True, default=uuid.uuid4)
  class Meta:
    database = db

class User(BaseModel):
  name = CharField()
  email = CharField()
  passwordHash = CharField()

class Course(BaseModel):
  name = CharField()
  description = TextField(null=True)
  owner = ForeignKeyField(User, backref='courses')
  due = DateField()
  status = CharField()
  syllabus = JSONField(null=True)

  def is_owned_by(self, user_uuid):
    return self.owner.id == str(user_uuid)

class Topic(BaseModel):
  name = CharField()

class Resource(BaseModel):
  name = CharField()
  url = CharField()
  votes = IntegerField(default=0)
  isBroken = IntegerField(default=0)

class ResourceTopic(BaseModel):
  topic = ForeignKeyField(Topic)
  resource = ForeignKeyField(Resource)

def initModels():
  db.create_tables([User, Course, Topic, Resource], safe=True)