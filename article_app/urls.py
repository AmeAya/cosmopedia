from django.urls import path
from .views import *

urlpatterns = [
    path('articles/', ArticleApiView.as_view()),
    path('auth/', AuthApiView.as_view()),
]
