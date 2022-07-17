from django.http import HttpResponse, JsonResponse
from .models import Resource
from rest_framework import viewsets, serializers

# def index(request):
#   resources = Resource.objects.order_by('-created_at').all()
#   return JsonResponse({"resources": list(resources.values())})

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Resource
    fields = ['id', 'title', 'url', 'votes']


class ResourceViewSet(viewsets.ModelViewSet):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer