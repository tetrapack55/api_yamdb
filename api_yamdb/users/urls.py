from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import GetToken, SignUp, UserViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
]
