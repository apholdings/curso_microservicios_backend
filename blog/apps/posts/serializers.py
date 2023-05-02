from rest_framework import serializers
from .models import Author, Post, ViewCount, Rate
from apps.category.serializers import CategorySerializer  # Import CategorySerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'username','picture']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'rate_number', 'user', 'post']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    rating=serializers.IntegerField(source='get_rating')
    rating_number=serializers.IntegerField(source='get_no_rating')
    category = CategorySerializer()  # Use CategorySerializer for category field
    sub_category = CategorySerializer()  # Use CategorySerializer for sub_category field
    topic = CategorySerializer()  # Use CategorySerializer for topic field

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'short_description', 'thumbnail', 'content',
            'created_at', 'updated_at', 'author', 'keywords', 'slug', 'rating_number',
            'language', 'level', 'views', 'clicks', 'impressions', 'category',
            'sub_category', 'topic', 'status', 'rating',
        ]


class ViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCount
        fields = ['id', 'post', 'ip_address']