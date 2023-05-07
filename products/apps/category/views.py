from apps.category.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category, ViewCount
from rest_framework.pagination import PageNumberPagination
from slugify import slugify
from django.core.cache import cache


class PrimaryCategoriesView(StandardAPIView):
    def get(self, request, format=None):
        primary_categories = Category.objects.filter(parent=None)
        category_names = [category.name for category in primary_categories]
        return self.send_response(category_names, status=status.HTTP_200_OK)
    

class SubCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slug)
            sub_categories = parent_category.children.all()
            sub_category_names = [category.name for category in sub_categories]
            return self.send_response(sub_category_names, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return self.send_error("Parent category does not exist.", status=status.HTTP_404_NOT_FOUND)


class TertiaryCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slug)
            print(parent_category)
            tertiary_categories = parent_category.children.all()
            tertiary_category_names = [category.name for category in tertiary_categories]
            return self.send_response(tertiary_category_names, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return self.send_error("Parent category does not exist.", status=status.HTTP_404_NOT_FOUND)


class ListCategoriesView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Category.objects.all().exists():
            categories = Category.objects.all()

            result = []

            for category in categories:
                if not category.parent:
                    item = {}
                    item['id']=category.id
                    item['name']=category.name
                    item['title']=category.title
                    item['description']=category.description
                    item['slug']=category.slug
                    item['views']=category.views
                
                    item['sub_categories'] = []
                    for sub_category in categories:
                        sub_item = {}
                        if sub_category.parent and sub_category.parent.id == category.id:
                            sub_item['id']=sub_category.id
                            sub_item['name']=sub_category.name
                            sub_item['title']=sub_category.title
                            sub_item['description']=sub_category.description
                            sub_item['slug']=sub_category.slug
                            sub_item['views']=sub_category.views

                            item['sub_categories'].append(sub_item)

                            sub_item['sub_categories'] = []
                            for sub_sub_category in categories.filter(parent=sub_category):
                                sub_sub_item = {}
                                if sub_sub_category.parent and sub_sub_category.parent.id == sub_category.id:
                                    sub_sub_item['id'] = sub_sub_category.id
                                    sub_sub_item['name'] = sub_sub_category.name
                                    sub_sub_item['title'] = sub_sub_category.title
                                    sub_sub_item['description'] = sub_sub_category.description
                                    sub_sub_item['slug'] = sub_sub_category.slug
                                    sub_sub_item['views']= sub_sub_category.views
                                    
                                    sub_item['sub_categories'].append(sub_sub_item)
                    
                    result.append(item)

            return self.send_response(result, status=status.HTTP_200_OK)
        else:
            return self.send_error('No categories found', status=status.HTTP_404_NOT_FOUND)


class ListPopularTopicsView(StandardAPIView):
    def get(self, request, format=None):
        cache_key = "popular_topics"
        popular_topics = cache.get(cache_key)

        if popular_topics is None:
            categories = Category.objects.order_by('views').all()[:int(6)]
            serializer = CategorySerializer(categories, many=True)
            cache.set(cache_key, serializer.data, 900)  # Cache for 15 minutes
            return self.send_response(serializer.data, status=status.HTTP_200_OK)
        else:
            return self.send_response(popular_topics, status=status.HTTP_200_OK)



class CategoryCreateView(StandardAPIView):
    permission_classes = (permissions.IsAdminUser,)
    def post(self, request, format=None):

        data = self.request.data
        name = data['name']
        slug = data['slug']
        slug = slugify(slug)
        thumbnail = data['thumbnail']
        Category.objects.create(name=name,thumbnail=thumbnail,slug=slug)

        return self.send_response('Category Created', status=status.HTTP_200_OK)


class CategoryEditView(StandardAPIView):
    permission_classes = (permissions.IsAdminUser,)
    def put(self, request, format=None):

        data = self.request.data
        category_id = data['category_id']
        name = data['name']
        category = Category.objects.get(id=category_id)

        category.name = name
        category.save()

        serializer = CategorySerializer(category)
        return self.send_response(serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteView(StandardAPIView):
    permission_classes = (permissions.IsAdminUser,)
    def delete(self, request, format=None):
        data = self.request.data
        category_id = data['category_id']
        category = Category.objects.get(id=category_id)
        category.delete()
        return self.send_response('Category deleted', status=status.HTTP_200_OK)
    

class CategoryDetailView(StandardAPIView):
    def get(self, request, slug, format=None):
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category)

        address = request.META.get('HTTP_X_FORWARDED_FOR')
        if address:
            ip = address.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        
        if not ViewCount.objects.filter(category=category, ip_address=ip):
            category.views += 1
            category.save()
            view = ViewCount(category=category,ip_address=ip)
            view.save()

        if Category.objects.filter(parent=category).exists():
            
            sub_categories = Category.objects.filter(parent=category)

            result = []

            for category in sub_categories:
                
                item = {}
                item['id'] = category.id
                item['name'] = category.name
                item['title'] = category.title
                item['description'] = category.description
                item['views'] = category.views
                item['slug'] = category.slug

                item['sub_categories'] = []

                for cat in sub_categories:
                    sub_item = {}
                    if cat.parent and cat.parent.id == category.id:
                        sub_item['id'] = cat.id
                        sub_item['name'] = cat.name
                        sub_item['title'] = cat.title
                        sub_item['description'] = cat.description
                        sub_item['views'] = cat.views
                        sub_item['slug'] = cat.slug

                        item['sub_categories'].append(sub_item)

                result.append(item)

            address = request.META.get('HTTP_X_FORWARDED_FOR')

            return self.send_response({
                'category': serializer.data,
                'sub_categories':result
                }, status=status.HTTP_200_OK)
        else:
            
            return self.send_response({
                    'category': serializer.data
                    # 'sub_categories':result
                    }, status=status.HTTP_200_OK)