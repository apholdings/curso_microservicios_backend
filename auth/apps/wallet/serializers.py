from rest_framework import serializers
from apps.user.serializers import UserSerializer
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Wallet
        fields = ('user', 'address', 'private_key')