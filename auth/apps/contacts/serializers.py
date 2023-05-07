from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import (
    SellerContact, InstructorContact, FriendContact,
    SellerContactList, InstructorContactList, FriendContactList,Contact
)

class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ContactSerializer(serializers.ModelSerializer):
    user = UserContactSerializer()
    contact = UserContactSerializer()

    class Meta:
        abstract = True
        model = Contact
        fields = ('user', 'contact', 'date_created')

class SellerContactSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = SellerContact

class InstructorContactSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = InstructorContact

class FriendContactSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = FriendContact

class SellerContactListSerializer(serializers.ModelSerializer):
    contacts = SellerContactSerializer(many=True)

    class Meta:
        model = SellerContactList
        fields = ('user', 'contacts')

class InstructorContactListSerializer(serializers.ModelSerializer):
    contacts = InstructorContactSerializer(many=True)

    class Meta:
        model = InstructorContactList
        fields = ('user', 'contacts')

class FriendContactListSerializer(serializers.ModelSerializer):
    contacts = FriendContactSerializer(many=True)

    class Meta:
        model = FriendContactList
        fields = ('user', 'contacts')