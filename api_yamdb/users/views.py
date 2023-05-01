# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserSerializer


class SignUp(APIView):
    def post(self, request):
        pass


class GetToken(TokenViewBase):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated,
                          IsAdmin,)

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = UserSerializer(self.request.user,
                                        data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
