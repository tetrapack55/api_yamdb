from django.db import models

from api.validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField("Год", validators=[validate_year])
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        related_name='titles',
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year',
            ),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.title} {self.genre}'
