from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from .models import Article
from .serializers import ArticleSerializer, UserSerializer, UserUpdateSerializer

from django.contrib.auth import login, logout, authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ArticleApiView(APIView):
    permission_classes = [IsAuthenticated, ]  # Апи выдает ответ только авторизованным пользователям

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: ArticleSerializer()
        }
    )  # in_ - каким образом этот параметр нам передается. Для ГЕТ это всегда openapi.IN_QUERY
    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            articles = articles.order_by(ordering)
        data = ArticleSerializer(articles, many=True).data  # instance = articles
        return Response(data, HTTP_200_OK)


class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'Welcome!',
            403: 'Username or/and Password is not valid!',
        }
    )
    def post(self, request):  # Авторизация
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, HTTP_200_OK)
        else:
            data = {'message': 'Username or/and Password is not valid!'}
            return Response(data, HTTP_403_FORBIDDEN)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):  # READ личный кабинет
        user = request.user
        data = UserSerializer(user).data
        return Response(data, status=HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer(),
        responses={
            200: UserSerializer(),
            400: '',
        }
    )
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = UserSerializer(user).data
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
