from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from .models import Article
from category_app.models import Category
from .serializers import *

from django.contrib.auth import login, logout, authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SelfArticleApiView(APIView):
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
    def patch(self, request):  # UPDATE USER
        user = request.user
        serializer = UserUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = UserSerializer(user).data
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):  # DELETE USER
        user = request.user
        if 'reason' in request.data.keys():
            print(user.username, request.data['reason'])
        user.delete()
        return Response({'message': 'User is deleted!'}, status=HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()  # Вызывается метод create у сериалайзера
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ArticleApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False,
                              description='Отправляем название филда по которому нужно расставить'),
            openapi.Parameter(name='category', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={
            200: ArticleSerializer()
        }
    )
    def get(self, request):
        articles = Article.objects.all()
        import random
        print(random.sample(list(articles), 2))
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            articles = articles.order_by(ordering)
        if 'category' in request.GET.keys():
            category_id = request.GET.get('category')
            category = Category.objects.get(id=category_id)
            articles = articles.filter(category=category)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            articles = articles.filter(title__contains=search).union(articles.filter(text__contains=search))
            # <field>.contains=<str> => Возвращает только те записи, у которых в <field> содержится строка <str>
            # objects.filter и objects.all возвращают QuerySet(Подобие set в python). А значит для них работают:
            # union, difference, symmetric_difference, intersection
        data = ArticleSerializer(articles, many=True).data
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            request.data['author'] = request.user.pk  # Вручную добавили в data новый ключ
            serializer = ArticleCreateSerializer(data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'message': 'Вы должны авторизоваться'}, status=HTTP_403_FORBIDDEN)


class ArticleDetailApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        data = ArticleSerializer(article, many=False).data
        return Response(data, status=HTTP_200_OK)

    def patch(self, request, article_id):
        article = Article.objects.get(id=article_id)
        # print(type(request.user))  # SimpleLazyObject - это ярлык, лишь ссылка на юзера, а не сам юзер
        # print(type(article.author))  # models.User - объект модели django user
        if request.user == article.author or request.user.is_staff:
            # == работает потому что сравнивает по значению. А is не работает потому что сравнивает по типу
            serializer = ArticleUpdateSerializer(article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = ArticleSerializer(article, many=False).data
                return Response(data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'message': 'Вы не автор статьи'}, status=HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = Article.objects.get(id=article_id)
        if request.user == article.author:
            article.delete()
            return Response({'message': 'Статья успешно удалена'}, status=HTTP_200_OK)
        return Response({'message': 'Вы не автор статьи'}, status=HTTP_403_FORBIDDEN)
