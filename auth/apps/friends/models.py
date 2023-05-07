from django.db import models
from django.conf import settings
from djoser.signals import  user_registered
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.user_profile.models import Profile
from django.core.exceptions import ObjectDoesNotExist


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_requests_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            profile = Profile.objects.get(user=self.from_user)
            picture_url = profile.picture.url
        except ObjectDoesNotExist:
            picture_url = None

        # Send message to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"friends_{self.to_user.id}",  # client's channel name
            {
                'type': 'send_friend_request',
                'message': {
                    'id': str(self.from_user_id),
                    'username': self.from_user.username,
                    'first_name': self.from_user.first_name,
                    'last_name': self.from_user.last_name,
                    'verified': self.from_user.verified,
                    'picture': picture_url
                },
            },
        )

    def cancel(self):
        self.delete()

    def archive(self):
        self.is_archived = True
        self.save()
    
    def accept(self):
        self.is_accepted = True
        self.archive()


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username
    
def post_user_registered(request, user ,*args, **kwargs):
    #1. Definir usuario que ser registra
    user = user
    FriendList.objects.create(user=user)

user_registered.connect(post_user_registered)