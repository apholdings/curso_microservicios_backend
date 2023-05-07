import re
from rest_framework_api.views import StandardAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile
from .serializers import UserProfileSerializer
from django.core.cache import cache
from django.contrib.auth import get_user_model
User = get_user_model()


pattern_special_characters = r'\badmin\b|[!@#$%^&*()_+-=[]{}|;:",.<>/?]|\s'


class MyUserProfileView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        serializer = UserProfileSerializer(profile).data
        return self.send_response(serializer,status=status.HTTP_200_OK)
    

class GetUserProfileView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, slug, *args, **kwargs):
        print(slug)
        return self.send_response('profile_data')


class EditUsernameView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self,request,format=None):

        data = self.request.data
        # Define User
        user = self.request.user
        user_model = User.objects.get(id=user.id)
        
        username = data['username']

        if re.search(pattern_special_characters, username, re.IGNORECASE) is None:
            user_model.username = username
            user_model.slug = username
            user_model.save()
            
            return self.send_response('Success',status=status.HTTP_200_OK)
        else:
            return self.send_error('Error',status.HTTP_400_BAD_REQUEST)