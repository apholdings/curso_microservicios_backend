from rest_framework import serializers

from apps.shipping.serializers import ShippingSerializer
from apps.category.serializers import CategorySerializer

from .models import *


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields =[
            'author',
            "address",
        ]


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            'id',
            'title',
            'price',
            'hex',
            'inStock',
            "position_id",
        ]


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = [
            'id',
            'title',
            'body',
            "position_id",
        ]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'id',
            'title',
            'price',
            'inStock',
            'stock',
            "position_id",
        ]

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'id',
            'title',
            'image',
            'price',
            'inStock',
            'stock',
            "position_id",
        ]

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = [
            'id',
            'title',
            'price',
            'inStock',
            'stock',
            "position_id",
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields =[
            'id',
            'position_id',
            "title",
            'file',
            'product',
        ]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields =[
            'id',
            'position_id',
            "title",
            'file',
            'product',
        ]


class BenefitssSerializer(serializers.ModelSerializer):
    class Meta:
        model= Benefits
        fields = [
            "id",
            "position_id",
            "title",
        ]


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Requisite
        fields = [
            "id",
            "position_id",
            "title",
        ]


class WhoIsForSerializer(serializers.ModelSerializer):
    class Meta:
        model= WhoIsFor
        fields = [
            "id",
            "position_id",
            "title",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    colors=ColorSerializer(many=True)
    details=DetailSerializer(many=True)
    sizes=SizeSerializer(many=True)
    rating=serializers.IntegerField(source='get_rating')
    rating_no=serializers.IntegerField(source='get_no_rating')
    shipping = ShippingSerializer(many=True)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    category=CategorySerializer()
    sellers=SellerSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'images',
            'colors',
            'details',
            'sizes',
            'rating',
            'rating_no',
            'shipping',
            'images',
            'videos',
            'category',
            'sellers',
            'token_id',
            'nft_address',
            'title',
            'description',
            'short_description',
            'price',
            'compare_price',
            'stock',
            'created_at',
            'updated_at',
            'business_activity',
            'type',
            'onSale',
        ]


class ProductListSerializer(serializers.ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    rating_no=serializers.IntegerField(source='get_no_rating')
    image=serializers.ImageField(source='get_image')
    shipping = ShippingSerializer(many=True)
    category=serializers.CharField(source='get_category_name')
    class Meta:
        model = Product
        fields = [
            'id',
            'image',
            'rating',
            'rating_no',
            'shipping',
            'category',
            'token_id',
            'nft_address',
            'title',
            'short_description',
            'price',
            'compare_price',
            'created_at',
            'updated_at',
            'onSale',
        ]