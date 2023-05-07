from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Shipping
from .serializers import ShippingSerializer
from django.core.cache import cache
from apps.product.models import Product
from apps.product.serializers import *
import jwt
from django.http import Http404
from rest_framework_api.views import StandardAPIView
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django.shortcuts import get_object_or_404
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


def get_product_data(id, user_id):
    try:
        product = Product.objects.get(id=id, author=user_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    videos = VideoSerializer(product.videos.all(), many=True)
    images = ImageSerializer(product.images.all(), many=True)
    shipping = ShippingSerializer(product.shipping.all(), many=True)
    documents = DocumentSerializer(product.documents.all(), many=True)
    colors = ColorSerializer(product.colors.all(), many=True)
    details = DetailSerializer(product.details.all(), many=True)
    sizes = SizeSerializer(product.sizes.all(), many=True)
    weights = WeightSerializer(product.weights.all(), many=True)
    materials = MaterialSerializer(product.materials.all(), many=True)

    whatlearnt = WhatLearntSerializer(product.what_learnt.all(), many=True)
    requisites = RequisiteSerializer(product.requisites.all(), many=True)
    who_is_for = WhoIsForSerializer(product.who_is_for.all(), many=True)
    resources = ResourceSerializer(product.resources.all(), many=True)

    product = ProductSerializer(product)

    product_data = {
        'videos': videos.data,
        'images': images.data,
        'shipping': shipping.data,
        'documents': documents.data,
        'detail': details.data,
        'colors': colors.data,
        'weights': weights.data,
        'materials': materials.data,
        'sizes': sizes.data,
        'whatlearnt': whatlearnt.data,
        'requisites': requisites.data,
        'who_is_for': who_is_for.data,
        'resources': resources.data,
        'details': product.data,
    }

    return product_data


class ListShippingOptionsView(APIView):
    def get(self, request, format=None):
        if Shipping.objects.all().exists():
            shipping_options = Shipping.objects.order_by('price').all()
            shipping_options = ShippingSerializer(shipping_options, many=True)
            return Response(
                {'shipping_options': shipping_options.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No shipping options available'},
                status=status.HTTP_404_NOT_FOUND
            )
        

class GetShippingView(StandardAPIView):
    def get(self, request, id, format=None):
        try:
            shipping = Shipping.objects.get(id=id)
            serializer = ShippingSerializer(shipping).data
            return self.send_response(serializer)
        except Shipping.DoesNotExist:
            return self.send_error('Shipping not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return self.send_error(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UpdateShippingView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):

        payload = validate_token(request)
        user_id = payload['user_id']
        data = self.request.data

        try:
            product = get_object_or_404(Product, id=data['productUUID'], author=user_id)

            result = []
            for shipping in data['shippingList']:
                if shipping['title'] == "":
                    continue 
                obj, created = Shipping.objects.update_or_create(
                    id=shipping['id'], author=user_id, product=product,
                    defaults={'title': shipping['title'], 'position_id':shipping['position_id'],'price':shipping['price'],'time':shipping['time']},
                )
                result.append(obj)

                if(created):
                    product.shipping.add(obj)

            product_data = get_product_data(product.id, user_id)

            return self.send_response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return self.send_error('Course with this ID does not exist or user_id did not match with course author',status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return self.send_error(str(e), status=status.HTTP_403_FORBIDDEN)
        except:
            return self.send_error('Bad Request',status=status.HTTP_400_BAD_REQUEST)


class DeleteShippingView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        payload = validate_token(request)
        user_id = payload['user_id']

        try:
            product = Product.objects.get(id=self.request.data['productUUID'], author=user_id)
        except Product.DoesNotExist:
            return self.send_error("Product not found.", status=status.HTTP_404_NOT_FOUND)

        try:
            shipping = Shipping.objects.get(id=self.request.data['id'],author = user_id)
        except Shipping.DoesNotExist:
            return self.send_error("Requisite not found.", status=status.HTTP_404_NOT_FOUND)

        if str(product.author) == user_id:
            if Product.objects.filter(shipping=shipping).exists():
                shipping.delete()
                product_data = get_product_data(product.id, user_id)
                return self.send_response(product_data, status=status.HTTP_200_OK)
            else:
                return self.send_error('That item does not exist.', status=status.HTTP_404_NOT_FOUND)
        else:
            return self.send_error('Only the course author may delete this', status=status.HTTP_401_UNAUTHORIZED)
        