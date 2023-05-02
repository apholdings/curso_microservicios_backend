# auth/apps/user_profile/models.py
from django.conf import settings
User = settings.AUTH_USER_MODEL

from djoser.signals import  user_registered

from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    picture = models.ImageField(default='media/users/user_default_profile.png',  upload_to='media/users/pictures/', blank=True, null=True, verbose_name='Picture')
    banner = models.ImageField(default='media/users/user_default_bg.jpg', upload_to='media/users/banners/' , blank=True, null=True, verbose_name='Banner')

    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)

    facebook = models.CharField(max_length=80, null=True, blank=True)
    twitter = models.CharField(max_length=80, null=True, blank=True)
    instagram = models.CharField(max_length=80, null=True, blank=True)
    linkedin = models.CharField(max_length=80, null=True, blank=True)
    youtube = models.CharField(max_length=80, null=True, blank=True)
    github = models.CharField(max_length=80, null=True, blank=True)


def post_user_registered(request, user ,*args, **kwargs):
    #1. Definir usuario que ser registra
    user = user
    Profile.objects.create(user=user)

user_registered.connect(post_user_registered)