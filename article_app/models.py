from django.db import models
from django.contrib.auth.models import User
from category_app.models import Category


class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
#     comments
