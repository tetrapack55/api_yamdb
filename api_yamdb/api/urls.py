from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)

v1 = routers.DefaultRouter()
v1.register('titles', TitleViewSet, basename='titles')
v1.register('categories', CategoryViewSet, basename='categories')
v1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(v1.urls)),
]