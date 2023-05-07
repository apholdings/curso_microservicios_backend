from rest_framework_api.views import StandardAPIView
import json, uuid
from rest_framework import serializers
from rest_framework import permissions
from .serializers import UserSerializer
from apps.user_profile.serializers import UserProfileSerializer
from apps.user_profile.models import Profile
from django.db import models
from django.core.cache import cache

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    
class ListAllUsersView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_data = UserSerializer(users, many=True).data
        return self.paginate_response(request, json.dumps(user_data, cls=UUIDEncoder))
    

class GetUserView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id, *args, **kwargs):
        cache_key = f'user_{id}'
        user_data = cache.get(cache_key)

        if not user_data:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user).data
            user_data = serializer
            cache.set(cache_key, user_data, 60 * 15)  # Cache for 15 minutes

        return self.send_response(user_data)
    

class GetUserProfileView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, slug, *args, **kwargs):
        print(slug)
        return self.send_response('profile_data')


class GetUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user.id')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    slug = serializers.CharField(source='user.slug')
    verified = serializers.BooleanField(source='user.verified')
    picture = serializers.ImageField(source='user.profile.picture')

    is_online = serializers.BooleanField(source='user.is_online')
    
    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'slug', 'verified', 'picture', 'is_online']
    
class GetUserDetailsView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, id, *args, **kwargs):
        user = User.objects.prefetch_related('profile', 'wallet').get(id=id)
        serializer = UserProfileSerializer(user.profile)
        return self.send_response(serializer.data)