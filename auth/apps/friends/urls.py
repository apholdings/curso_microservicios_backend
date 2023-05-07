from django.urls import path

from .views import *


urlpatterns = [
    path('add_friend/', SendFriendRequest.as_view()),
    path('remove_friend/', RemoveFriend.as_view()),
    path('cancel_friend_request/', CancelFriendRequest.as_view()),
    path('accept/', AcceptRequest.as_view(), name='accept-friend-request'),
    path('friend-requests/check-sent/', CheckRequestSentView.as_view(), name='check_friend_request_sent'),
    path('check-users-are-friends/', CheckUsersAreFriendsView.as_view(), name='check-users-are-friends')
]