from django.contrib import admin

from .models import Resource, Topic

admin.site.register([Resource, Topic])
