from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       CommentViewSet,
                       ReviewViewSet,
                       TitleViewSet,
                       UserViewSet,
                       GenreViewSet,
                       get_token,
                       signup)

app_name = 'api'

v1 = routers.DefaultRouter()
v1.register('titles', TitleViewSet, basename='titles')
v1.register('categories', CategoryViewSet, basename='categories')
v1.register('genres', GenreViewSet, basename='genres')
v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
