from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'Проверьте год создания произведения (должен быть нашей эры).'
            )
        return value

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
