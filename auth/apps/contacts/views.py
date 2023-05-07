from rest_framework_api.views import StandardAPIView
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import Q


class GetMyContactListsView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user

        # Get or create Contact lists
        seller_contact_list, _ = SellerContactList.objects.get_or_create(user=user)
        instructor_contact_list, _ = InstructorContactList.objects.get_or_create(user=user)
        friend_contact_list, _ = FriendContactList.objects.get_or_create(user=user)

        # Serialize contact lists
        seller_contact_list_serializer = SellerContactListSerializer(seller_contact_list)
        instructor_contact_list_serializer = InstructorContactListSerializer(instructor_contact_list)
        friend_contact_list_serializer = FriendContactListSerializer(friend_contact_list)
        
        return self.send_response({
            'seller_contact_list': seller_contact_list_serializer.data,
            'instructor_contact_list': instructor_contact_list_serializer.data,
            'friend_contact_list': friend_contact_list_serializer.data,
        }, status=status.HTTP_200_OK)

