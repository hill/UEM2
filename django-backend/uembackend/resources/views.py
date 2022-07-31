from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from .models import Resource
from rest_framework import viewsets, serializers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "title", "url", "votes", "created_by"]
        read_only_fields = ["created_at", "created_by"]
        extra_kwargs = {"created_by": {"default": serializers.CurrentUserDefault()}}


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"])
    def upvote(self, request, pk=None):
        resource = self.get_object()
        resource.upvote(request.user.profile)
        return Response({"status": "ok"})

    @action(detail=True, methods=["post"])
    def save(self, request, pk=None):
        resource = self.get_object()
        request.user.profile.save_resource(resource)
        return Response({"status": "ok"})

    @action(detail=False, methods=["get"])
    def saved_resources(self, request):
        saved = request.user.profile.saved_resources.all()
        print(saved[0])
        serializer = ResourceSerializer(saved, many=True)
        return JsonResponse({"resources": serializer.data})

    @action(detail=True, methods=["post"])
    def broken(self, request, pk=None):
        resource = self.get_object()
        resource.is_broken_votes += 1
        resource.save()
        return Response({"status": "ok"})


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user"""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get("user", {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
