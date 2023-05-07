import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from apps.user_profile.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ObjectDoesNotExist
import uuid

class FriendsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope['query_string'].decode('utf-8').split('=')[1]
        self.group_name = f"friends_{self.user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'get_friendslist':
            # Fetch friends for user
            start = int(text_data_json.get('start', 0))
            count = int(text_data_json.get('count', 20))
            friends = await self.get_friendslist(start, count)
            await self.send_friendslist(friends)
        
        elif message_type == 'get_friend_requests':
            # Get friend requests for user
            start = int(text_data_json.get('start', 0))
            count = int(text_data_json.get('count', 20))
            friend_requests = await self.get_friend_requests(start,count)
            # Send friend requests to WebSocket
            await self.send_friend_requests(friend_requests)

        elif message_type == 'check_friend':
            message = text_data_json["message"]
            check_friends_request = await self.check_friends(message)

            # Send friend requests to WebSocket
            await self.send_check_friends(check_friends_request)

        elif message_type == 'accept_friend_request':
            friend_request_id = text_data_json.get('friend_request_id')
            result = await self.accept_friend_request(friend_request_id)
            if result['success']:
                friends = await self.get_friendslist(0, 20)
                await self.send_friendslist(friends)
            await self.send(text_data=json.dumps(result))

        elif message_type == 'cancel_friend_request':
            message = text_data_json["message"]
            print(message)
            event = {
                'type': 'cancel_friend_request',
                'message': message
            }
            # send message to group
            await self.channel_layer.group_send(self.group_name, event)
        
        else:
            message = text_data_json["message"]
            event = {
                'type': 'send_message',
                'message': message
            }
            # send message to group
            await self.channel_layer.group_send(self.group_name, event)

    @database_sync_to_async
    def get_friendslist(self, start, count):
        friend_list = FriendList.objects.get(user_id=self.user_id)
        friends = friend_list.friends.all()[start:start+count]
        friends_data = []

        for friend in friends:
            try:
                profile = Profile.objects.get(user=friend)
                picture_url = profile.picture.url
            except ObjectDoesNotExist:
                picture_url = None

            friends_data.append({
                'id': str(friend.id),
                'username': friend.username,
                'email': friend.email,
                'picture': picture_url
            })

        return friends_data
    
    
    @database_sync_to_async
    def get_friend_requests(self, start, count):
        friend_requests = FriendRequest.objects.filter(to_user_id=self.user_id, is_archived=False, is_accepted=False)[start:start+count]
        friend_requests_data = []

        for request in friend_requests:
            try:
                profile = Profile.objects.get(user=request.from_user)
                picture_url = profile.picture.url
            except ObjectDoesNotExist:
                picture_url = None

            friend_requests_data.append({
                'id': str(request.from_user_id),
                'username': request.from_user.username,
                'first_name': request.from_user.first_name,
                'last_name': request.from_user.last_name,
                'verified': request.from_user.verified,
                'picture': picture_url
            })

        return friend_requests_data

    @database_sync_to_async
    def check_friends(self, friend_id):
        # Get the email of the user to check
        user_id = self.user_id
        
        friend = User.objects.get(id=friend_id)

        # Check if they are friends
        friends_list = FriendList.objects.get(user_id=user_id)
        if friend in friends_list.friends.all():
            # return Response({'are_friends': True})
            return {
                'type': 'check_friend',
                'is_friend': True,
                'total_count': 1,
            }
        else:
            return {
                'type': 'check_friend',
                'is_friend': False,
                'total_count': 0,
            }
        

    async def send_check_friends(self, event):
        is_friend = event['is_friend']
        message = {
            'type': 'check_friend',
            'data': is_friend
        }
        await self.send(text_data=json.dumps(message))  

    @database_sync_to_async
    def get_friend_request_count(self):
        return FriendRequest.objects.filter(to_user_id=self.user_id, is_archived=False, is_accepted=False).count()
    
    @database_sync_to_async
    def accept_friend_request(self, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user_id=self.user_id)
        except FriendRequest.DoesNotExist:
            return {'success': False, 'message': 'Friend request not found.'}
        friend_request.accept()
        return {'success': True, 'message': 'Friend request accepted.'}

    @database_sync_to_async
    def decline_friend_request(self, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user_id=self.user_id)
        except FriendRequest.DoesNotExist:
            return {'success': False, 'message': 'Friend request not found.'}
        friend_request.decline()
        return {'success': True, 'message': 'Friend request declined.'}
    
    async def send_message(self, event):
        message = event['message']
        # send message to websocket
        await self.send(text_data=json.dumps({'message':message}))

    async def send_friendslist(self, data):
        message = {
            'type': 'friends_list',
            'data': data
        }
        await self.send(text_data=json.dumps(message))

    async def send_friend_requests(self, data):
        total_count = await self.get_friend_request_count()
        message = {
            'type': 'friend_requests',
            'data': data,
            'total_count': total_count
        }
        await self.send(text_data=json.dumps(message))
    
    async def send_friend_request(self, event):
        message = event['message']
        friend_request= {
            'id':str(message.get('id')),
            'username':str(message.get('username')),
            'first_name':str(message.get('first_name')),
            'last_name':str(message.get('last_name')),
            'verified':str(message.get('verified')),
            'picture': str(message.get('picture'))
        }
        total_count = await self.get_friend_request_count()
        message = {
            'type': 'new_friend_request',
            'data': friend_request,
            'total_count': total_count
        }
        # send message to websocket
        await self.send(text_data=json.dumps(message))
    
    async def cancel_friend_request(self, text_data):
        text_data_json = json.loads(text_data)
        friend_request_id = text_data_json.get('friend_request_id')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, from_user_id=self.user_id)
        except FriendRequest.DoesNotExist:
            return {'success': False, 'message': 'Friend request not found.'}
        friend_request.cancel()

        # Send message to WebSocket group of the user who sent the request
        try:
            profile = Profile.objects.get(user=friend_request.to_user)
            picture_url = profile.picture.url
        except ObjectDoesNotExist:
            picture_url = None

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"friends_{friend_request.to_user.id}",
            {
                'type': 'cancel_friend_request',
                'message': {
                    'id': str(friend_request.from_user_id),
                    'username': friend_request.from_user.username,
                    'first_name': friend_request.from_user.first_name,
                    'last_name': friend_request.from_user.last_name,
                    'verified': friend_request.from_user.verified,
                    'picture': picture_url
                },
            },
        )

        return {'success': True, 'message': 'Friend request cancelled.'}

    async def send_cancel_friend_request(self, event):
        message = event['message']
        friend_request= {
            'id':str(message.get('id')),
            'username':str(message.get('username')),
            'first_name':str(message.get('first_name')),
            'last_name':str(message.get('last_name')),
            'verified':str(message.get('verified')),
            'picture': str(message.get('picture'))
        }
        total_count = await self.get_friend_request_count()
        message = {
            'type': 'cancel_friend_request',
            'data': friend_request,
            'total_count': total_count
        }
        await self.send(text_data=json.dumps(message))


