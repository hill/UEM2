from django.db import models

class Topic(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Resource(models.Model):
  created_at = models.DateTimeField('created at', auto_now_add=True)
  modified_at = models.DateTimeField('modified at', auto_now=True)
  title = models.CharField(max_length=200)
  url = models.URLField()
  votes = models.IntegerField(default=0)
  is_broken_votes = models.IntegerField(default=0)
  topics = models.ManyToManyField(Topic)

  def __str__(self):
    return self.title
