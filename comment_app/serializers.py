from rest_framework.serializers import ModelSerializer
from .models import Comment
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = representation['created_at'].split('.')[0].replace('T', ' ')
        representation['author'] = UserSerializer(instance.author).data
        return representation
