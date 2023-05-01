import re

from rest_framework import serializers 

from reviews.models import Category, Genre, Title
from .validators import validate_year


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")

    def validate_slug(self, value):
        if re.match(pattern=r"^[-a-zA-Z0-9_]+$", string=value):
            return value
        raise serializers.ValidationError(
            "Slug содержит запрещенные символы"
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")

    def validate_slug(self, value):
        if re.match(pattern=r"^[-a-zA-Z0-9_]+$", string=value):
            return value
        raise serializers.ValidationError(
            "В поле Slug содержится запрещенные символы"
        )


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

 