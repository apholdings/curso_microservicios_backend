from rest_framework import serializers
from .models import *

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'id',
            'name',
            'network',
            
            'symbol',
            'address',
            'decimals',
            'icon_url',
            'is_custom',
            'created_at',
        ]

class TokenBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenBalance
        fields = [
            'id',
            'balance',
        ]

class TokenListSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(many=True)
    class Meta:
        model = TokenList
        fields = [
            'id',
            'tokens',
            'address'
        ]