from rest_framework_api.views import StandardAPIView
from rest_framework import permissions, status
from django.core.cache import cache
from django.db.models import F
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
import jwt
from django.conf import settings
secret_key = settings.SECRET_KEY


def validate_token(request):
    token = request.META.get('HTTP_AUTHORIZATION').split()[1]
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({"error": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response({"error": "An error occurred while decoding the token."}, status=status.HTTP_401_UNAUTHORIZED)
    return payload


class ListPostsView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        cache_key = 'published_posts'
        posts_shown = cache.get(cache_key)

        if not posts_shown:
            posts_shown = Post.objects.filter(status='published')
            cache.set(cache_key, posts_shown, 900)  # Cache for 15 minutes

        Post.objects.filter(id__in=posts_shown).update(impressions=F('impressions') + 1)

        serializer = PostSerializer(posts_shown, many=True)
        return self.paginate_response(request, serializer.data)


class DetailPostView(StandardAPIView):
    def get(self, request, slug, *args, **kwargs):
        cache_key = f'post_detail_{slug}'
        post = cache.get(cache_key)

        if not post:
            post = Post.objects.get(slug=slug)
            cache.set(cache_key, post, 900)  # Cache for 15 minutes

        serializer = PostSerializer(post)
        return self.send_response(serializer.data)
    

class CreatePostView(StandardAPIView):
    def post(self, request, format=None):
        payload = validate_token(request)

        data = self.request.data

        if data.get('user').get('role') != 'editor':
            raise PermissionError('You dont have the permissions to create a post.')

        post = Post.objects.create(
            title = data['title'],
            short_description = data['short_description'],
            thumbnail = data['thumbnail'],
            content = data['content'],
            keywords = data['keywords'],
            slug = data['slug'],
        )

        serializer = PostSerializer(post).data
        return self.send_response(serializer.data,status=status.HTTP_201_CREATED)


class UpdatePostView(StandardAPIView):
    def put(self, request, format=None):
        payload = validate_token(request)
        data = self.request.data
        print(f'Payload: {payload} and Data: {data}')
        # if data.get('user').get('role') != 'editor':
        #     raise PermissionError('You dont have the permissions to create a post.')

        # post = Post.objects.create(
        #     title = data['title'],
        #     short_description = data['short_description'],
        #     thumbnail = data['thumbnail'],
        #     content = data['content'],
        #     keywords = data['keywords'],
        #     slug = data['slug'],
        # )

        # serializer = PostSerializer(post).data
        return self.send_response('serializer.data',status=status.HTTP_201_CREATED)


class DeletePostView(StandardAPIView):
    def delete(self, request, id, format=None):
        payload = validate_token(request)
        print(f'Payload: {payload} and Post ID: {id}')
        # if data.get('user').get('role') != 'editor':
        #     raise PermissionError('You dont have the permissions to create a post.')

        # post = Post.objects.create(
        #     title = data['title'],
        #     short_description = data['short_description'],
        #     thumbnail = data['thumbnail'],
        #     content = data['content'],
        #     keywords = data['keywords'],
        #     slug = data['slug'],
        # )

        # serializer = PostSerializer(post).data
        return self.send_response('serializer.data',status=status.HTTP_201_CREATED)