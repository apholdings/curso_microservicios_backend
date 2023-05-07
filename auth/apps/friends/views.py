from rest_framework import status
from rest_framework.response import Response
from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *
from apps.user.models import UserAccount
from core.producer import producer
import json
from .consumers import FriendsConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SendFriendRequest(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, format=None):
        # Get the email of the user to send a friend request to
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the receiver user object
        try:
            receiver = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with email {} does not exist'.format(email)}, status=status.HTTP_404_NOT_FOUND)

        sender = self.request.user

        if sender == receiver:
            return Response({'message': 'You cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a friend request has already been sent
        if FriendRequest.objects.filter(from_user=sender, to_user=receiver).exists():
            return Response({'message': 'You have already sent a friend request to {}'.format(receiver.username)}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new friend request
        FriendRequest.objects.create(from_user=sender, to_user=receiver)

        # # Create Notification Object through kafka producer
        # notification_data = {
        #     'from_user': str(sender.id),  # convert UUID to string
        #     'to_user': str(receiver.id),  # convert UUID to string
        #     'notification_type': 3,
        #     'text_preview': f"{sender.username} wants to be your friend.",
        #     'url': '/@'+sender.username,
        #     'is_seen': False,
        #     'icon': 'bx bx-user-circle',
        # }
        # producer.produce(
        #     'notifications',
        #     key='friend_request',
        #     value=json.dumps(notification_data).encode('utf-8')
        # )
        # # encode notification data as JSON and produce to Kafka topic
        # producer.flush()

        return self.send_response({'message': 'Friend request has been sent to {}'.format(receiver.username)}, status=status.HTTP_200_OK)
    



class CancelFriendRequest(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        # Get the email of the user to cancel friend request
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the receiver user object
        try:
            receiver = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with email {} does not exist'.format(email)}, status=status.HTTP_404_NOT_FOUND)

        sender = self.request.user

        # Check if a friend request has been sent
        try:
            friend_request = FriendRequest.objects.get(from_user=sender, to_user=receiver)
        except FriendRequest.DoesNotExist:
            return Response({'message': 'No friend request found for {} from {}'.format(receiver.username, sender.username)}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel the friend request
        friend_request.delete()

        return Response({'message': 'Friend request canceled'})



class RemoveFriend(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        email = request.data.get('email')
        try:
            friend = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.send_error({'message': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Remove the friend from each other's friend list
        try:
            request.user.friend_list.friends.remove(friend)
            friend.friend_list.friends.remove(request.user)

            # Get channel layer and group name
            channel_layer = get_channel_layer()
            group_name = f'friends_{friend.id}'

            # Send message to WebSocket group
            async_to_sync(channel_layer.group_send)(group_name, {
                'type': 'send_check_friends',
                'is_friend': False
            })

        except Exception as e:
            # Handle any exceptions that might occur during the process
            print(f"Error removing friend: {str(e)}")
            return self.send_error({'message': 'Failed to remove friend'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return self.send_response('Friend removed')


class AcceptRequest(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, format=None):
        friend_request_id=request.data['friend_request_id']
        action=request.data['action']
        try:
            friend_request = FriendRequest.objects.get(from_user__id=friend_request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return self.send_error({'message': 'Friend request does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        
        if action==True:
            friend_request.is_accepted = True
            friend_request.save()

            # Add the users to each other's friend list
            try:
                friend_request.from_user.friend_list.friends.add(request.user)
                request.user.friend_list.friends.add(friend_request.from_user)
            except Exception as e:
                # Handle any exceptions that might occur during the process
                print(f"Error adding users to friend list: {str(e)}")

            # Create Notification Object through kafka producer
            notification_data = {
                'from_user': str(friend_request.to_user.id),  # convert UUID to string
                'to_user': str(friend_request.from_user.id),  # convert UUID to string
                'notification_type': 3,
                'text_preview': f"{friend_request.to_user.username} accepted your friend request.",
                'url': '/@'+friend_request.to_user.username,
                'is_seen': False,
                'icon': 'bx bx-user-circle',
            }
            producer.produce(
                'notifications',
                key='friend_request',
                value=json.dumps(notification_data).encode('utf-8')
            )
            # encode notification data as JSON and produce to Kafka topic
            producer.flush()

            # Create message to send to WebSocket
            # message = {
            #     'type': 'send_check_friends',
            #     'is_friend': True
            # }
            
            # Get channel layer and group name
            channel_layer = get_channel_layer()
            group_name = f'friends_{friend_request.from_user.id}'

            # Send message to WebSocket group
            async_to_sync(channel_layer.group_send)(group_name, {
                'type': 'send_check_friends',
                'is_friend': True
            })
            friend_request.delete()
        else:
            friend_request.is_archived = True
            friend_request.save()

        # Notify the sender that the friend request is accepted
        try:
            user_id = request.user.id
            friend_requests = FriendRequest.objects.filter(to_user_id=user_id, is_archived=False, is_accepted=False)[0:0+20]
            friend_requests_count = FriendRequest.objects.filter(to_user_id=user_id, is_archived=False, is_accepted=False).count()

            # Create message to send to WebSocket
            message = {
                'type': 'send_friend_requests',
                'data': list(friend_requests.values()),
                'total_count': friend_requests_count
            }
            
            # Get channel layer and group name
            channel_layer = get_channel_layer()
            group_name = f'friends_{user_id}'

            # Send message to WebSocket group
            async_to_sync(channel_layer.group_send)(group_name, message)
            
        except Exception as e:
            # Handle any exceptions that might occur during the process
            print(f"Error sending group message: {str(e)}")
        
        return self.send_response('Friend request updated successfully', status=status.HTTP_200_OK)
        

class CheckRequestSentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format=None):
        # Get the email of the user to check
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user objects
        sender = self.request.user
        try:
            receiver = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with email {} does not exist'.format(email)}, status=status.HTTP_404_NOT_FOUND)

        # Check if a friend request has already been sent
        if FriendRequest.objects.filter(from_user=sender, to_user=receiver).exists():
            return Response({'request_sent': True})

        return Response({'request_sent': False})


class CheckUsersAreFriendsView(StandardAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # Get the email of the user to check
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user objects
        user = self.request.user
        try:
            friend = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with email {} does not exist'.format(email)}, status=status.HTTP_404_NOT_FOUND)

        # Check if they are friends
        friends_list = FriendList.objects.get(user=user)
        if friend in friends_list.friends.all():
            # return Response({'are_friends': True})
            return self.send_response(True, status=status.HTTP_200_OK)

        # return Response({'are_friends': False})
        return self.send_response(False, status=status.HTTP_200_OK)