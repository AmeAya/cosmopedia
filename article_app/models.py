from django.db import models
from django.contrib.auth.models import User
from category_app.models import Category
from comment_app.models import Comment


class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='articles')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(Comment, blank=True)
