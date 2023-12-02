from rest_framework.serializers import ModelSerializer
from .models import Article
from category_app.serializers import CategorySerializer
from django.contrib.auth.models import User
from comment_app.serializers import CommentSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):  # Вызывается с помощью методы .save()
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance) -> dict:
        # to_representation - Основной метод, который показывает как надо возвращать данные
        # instance - Объект, который надо сериализировать
        representation = super().to_representation(instance)  # Возвращает тип dict(словарь)
        representation['created_at'] = representation['created_at'].split('.')[0].replace('T', ' ')
        representation['author'] = UserSerializer(instance.author).data
        representation['category'] = CategorySerializer(instance.category, many=True).data
        representation['comments'] = CommentSerializer(instance.comments, many=True).data
        return representation


class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'category', 'author', 'image']


class ArticleUpdateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'category']
