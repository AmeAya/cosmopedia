"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

SchemaView = get_schema_view(
    info=openapi.Info(
        title='Cosmopedia',
        default_version='v1.0',
        description='This is encyclopedia about space terms',
        terms_of_service='',
        contact=openapi.Contact(name='Dias Bolatov', url='', email='deobackstep@gmail.com'),
        license=openapi.License(name='JustCode', url='')
    ),
    patterns=[
        path('category/', include('category_app.urls')),
        path('article/', include('article_app.urls')),
    ],
    public=True,
    permission_classes=[AllowAny, ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', include('category_app.urls')),
    path('article/', include('article_app.urls')),
    path('swagger/', SchemaView.with_ui()),
]
