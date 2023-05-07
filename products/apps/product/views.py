from rest_framework_api.views import StandardAPIView
from rest_framework import permissions, status
from django.core.cache import cache
from .models import *
from .serializers import *
from django.db.models import Q, F
from django.core.validators import validate_slug
from django.db.models import Avg
import base64, jwt, tempfile, rsa, secrets, json
from base64 import b64decode


class SearchProductsView(StandardAPIView):
    def get(self, request, *args, **kwargs):

        cache_key = f"search_products_{request.META['QUERY_STRING']}"
        cached_result = cache.get(cache_key)

        if cached_result:
            return self.paginate_response(request, cached_result)
        
        products = Product.objects.all()

        search = request.query_params.get('search', None)
        if search and 'null' not in search:
            products = Product.objects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) | 
                Q(short_description__icontains=search) | 
                Q(keywords__icontains=search) |
                Q(category__name__icontains=search) |
                Q(category__title__icontains=search) |
                Q(category__description__icontains=search) 
            )

        # Get Order parameter
        order_by = request.query_params.get('order', '-created_at')
        if order_by == 'oldest':
            products = products.order_by('created_at')
        elif order_by == 'desc':
            products = products.order_by('title')
        elif order_by == 'asc':
            products = products.order_by('-title')
        else:
            products = products.order_by(order_by)
        
        filter_by = request.query_params.get('filter', None)
        if filter_by == 'views':
            products = products.order_by('-views')
        elif filter_by == 'sold':
            products = products.order_by('-sold')
        elif filter_by == 'price':
            if order_by == 'asc':
                products = products.order_by('price')
            elif order_by == 'desc':
                products = products.order_by('-price')
        elif order_by == 'impressions':
            products = products.order_by('-impressions')
        elif order_by == 'clickThroughRate':
            products = products.order_by('-clickThroughRate')
        elif order_by == 'purchases':
            products = products.order_by('-purchases')
        elif order_by == 'conversion_rate':
            products = products.order_by('-conversion_rate')
        elif order_by == 'avg_time_on_page':
            products = products.order_by('-avg_time_on_page')

        category = request.query_params.getlist('category', None)
        if category and '' not in category:
            q_obj = Q()
            for cat in category:
                if cat.isdigit():  # If the value is a number
                    q_obj |= Q(category__id=cat) | Q(sub_category__id=cat) | Q(topic__id=cat)
                elif validate_slug(cat) is None:  # If the value is a slug
                    q_obj |= Q(category__slug=cat) | Q(sub_category__slug=cat) | Q(topic__slug=cat)
            products = products.filter(q_obj)

        rating = request.query_params.get('rating', None)
        products = products.annotate(avg_rating=Avg('rating__rate_number'))
        if rating and rating != 'undefined':
            products = products.filter(avg_rating__gte=float(rating))
        else:
            products = products.order_by('-avg_rating')

        pricing = request.query_params.get('pricing', None)
        if pricing and pricing != 'undefined':
            if pricing == 'Free':
                products = products.filter(price__lte=0)
            elif pricing == 'Paid':
                products = products.filter(price__gt=0)
        
        author = request.query_params.get('author', None)
        if author and author != '' and author != 'undefined'and author != 'null':
            products = products.filter(author=author)

        serializer = ProductListSerializer(products, many=True).data
        # Cache the result
        cache.set(cache_key, serializer, 1800)  # Cache for 1800 seconds
        return self.paginate_response(request, serializer)