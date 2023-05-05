import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from reviews.models import (Category, Comment, Genre,
                            Review, Title, GenreTitle)
from users.models import User

CSV_FILES = {Category: 'category.csv',
             Genre: 'genre.csv',
             Title: 'titles.csv',
             GenreTitle: 'genre_title.csv',
             User: 'users.csv',
             Review: 'review.csv',
             Comment: 'comments.csv'}

REPLACE_FIELDS = {Title: ['category', 'category_id'],
                  Review: ['author', 'author_id'],
                  Comment: ['author', 'author_id']}


class Command(BaseCommand):
    """Импорт данных из CSV_FILES"""

    def handle(self, *args, **options):
        '''Импорт в БД'''

        for model, csv_file in CSV_FILES.items():
            file = f'{settings.BASE_DIR}/static/data/{csv_file}'

            with open(f'{file}', 'r', encoding='utf8') as file:
                for row in csv.DictReader(file, delimiter=','):
                    if model in REPLACE_FIELDS:
                        row.update({
                            REPLACE_FIELDS[model][1]:
                            row.pop(REPLACE_FIELDS[model][0])
                        })

                    try:
                        model.objects.create(**row)
                    except ValueError as e:
                        raise CommandError(
                            f'Ошибка: {e}, файл {file}, строка {row}'
                        )
                    except IntegrityError as e:
                        raise CommandError(f'База данных уже заполнена. \n{e}')
            self.stdout.write(f'Файл с данными {csv_file} импортирован!')
