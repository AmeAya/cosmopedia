from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from .models import Article
from .serializer import ArticleSerializer

from django.contrib.auth import login, logout, authenticate


class ArticleApiView(APIView):
    permission_classes = [IsAuthenticated, ]  # Апи выдает ответ только авторизованным пользователям

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        data = ArticleSerializer(articles, many=True).data  # instance = articles
        return Response(data, HTTP_200_OK)


class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
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
