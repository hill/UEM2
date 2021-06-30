import uuid
from peewee import *
from playhouse.sqlite_ext import JSONField
db = SqliteDatabase('newDb.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
  id = CharField(primary_key=True, default=uuid.uuid4)
  class Meta:
    database = db
  
  def refresh(self):
    return type(self).get(self._pk_expr())

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
  name = CharField(unique=True)

class Resource(BaseModel):
  name = CharField()
  url = CharField()
  votes = IntegerField(default=0)
  isBroken = IntegerField(default=0)

  @classmethod
  def create(cls, **kwargs):
    topics = kwargs.pop('topics', None)
    new_resource = cls(**kwargs)
    new_resource.save(force_insert=True)

    if topics:
      for topic_name in topics:
        query = Topic.select().where(Topic.name == topic_name)
        if not query.exists():
          # create a topic if it doesn't exist
          topic = Topic.create(name=topic_name)
        else:
          topic = query
        # add the topic to the resource
        ResourceTopic.create(resource=new_resource, topic=topic)

    return new_resource

  @property
  def topics(self):
    return (Topic.select()
                  .join(ResourceTopic)
                  .join(Resource)
                  .where(Resource.id == self.id))

class ResourceTopic(BaseModel):
  topic = ForeignKeyField(Topic)
  resource = ForeignKeyField(Resource)

def initModels():
  db.create_tables([User, Course, Topic, Resource, ResourceTopic], safe=True)