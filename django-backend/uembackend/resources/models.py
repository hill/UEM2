from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Resource(models.Model):
    created_at = models.DateTimeField("created at", auto_now_add=True)
    modified_at = models.DateTimeField("modified at", auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_broken_votes = models.IntegerField(default=0)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title

    @property
    def votes(self):
        vote_count = Vote.objects.filter(resource=self).aggregate(models.Sum("value"))[
            "value__sum"
        ]
        return vote_count if vote_count else 0

    def upvote(self, user: "Profile"):
        # TODO: don't upvote if the vote already exists
        Vote(resource=self, user=user, value=1).save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_resources = models.ManyToManyField(Resource)

    def __str__(self):
        return self.user.username

    def save_resource(self, resource: Resource):
        self.saved_resources.add(resource)

    def unsave_resource(self, resource: Resource):
        self.saved_resources.remove(resource)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Vote(models.Model):
    created_at = models.DateTimeField("created at", auto_now_add=True)
    value = models.IntegerField(choices=[(1, "1"), (-1, "-1")])
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
