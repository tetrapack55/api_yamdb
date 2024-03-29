from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class SlugDictRelatedField(serializers.SlugRelatedField):
    """Сериализатор для корректного вывода данных при запросах."""

    def to_representation(self, obj):
        result = {"name": obj.name, "slug": obj.slug}
        return result


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = SlugDictRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = SlugDictRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        rating = self.context["rating"]
        if obj in rating:
            return rating.get(pk=obj.pk).rating


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError('Может существовать '
                                              'только один отзыв.')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.DEFAULT_EMAIL_LENGHT,
        required=True
    )
    username = serializers.CharField(
        max_length=settings.DEFAULT_USER_CHARFIELD,
        required=True,
        validators=[UnicodeUsernameValidator()]
    )

    def validate_username(self, value):
        username = value.lower()
        if username == 'me':
            raise ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
