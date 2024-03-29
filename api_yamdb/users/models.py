from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Никнейм',
        max_length=settings.DEFAULT_USER_CHARFIELD,
        blank=False,
        unique=True,
        validators=(username_validator,),
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.DEFAULT_USER_CHARFIELD,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.DEFAULT_USER_CHARFIELD,
        blank=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.DEFAULT_EMAIL_LENGHT,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=15,
        choices=ROLE_CHOICES,
        default=USER
    )
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username
