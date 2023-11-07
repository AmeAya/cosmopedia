from django.urls import path
from .views import *

urlpatterns = [
    path('api/', CategoryApiView.as_view(), name='category_url'),
    path('api/<int:pk>/', CategoryDetailApiView.as_view(), name='category_detail_url'),
]
