from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    # views=serializers.IntegerField(source='get_view_count')
    class Meta:
        model=Category
        fields=[
            'id',
            'name',
            'title',
            'description',
            'slug',
            'views',
        ]