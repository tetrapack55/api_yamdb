from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from api.filters import TitleFilter
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             CommentSerializer,
                             ReviewSerializer,)
from reviews.models import Category, Genre, Title, Review
from users.models import User
from users.permissions import (IsAdmin,
                               IsAdminOrReadOnly,
                               IsAdminOrModerOrAuthorOrReadOnly,)
from api.serializers import (GetTokenSerializer,
                             SignUpSerializer, UserSerializer)


class GetPostDeleteViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    pass


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        user, _ = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения для получения токена: {confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения!'},
                    status=status.HTTP_400_BAD_REQUEST)
