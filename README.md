# api_yamdb
api_yamdb

#Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.

Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

## Технологии, использованные при разработке
- python 3.7  
- Django 3.2
- djangorestframework 3.12.4  

## Установка
- Установить зависимости из файла requirements.txt

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
### Примеры API запросов:

Документация доступна по эндпоинту: /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения,
что-либо изменить или создать не получится.

- Выполнить миграции:

```
python manage.py migrate
```

- Создать суперпользователя:

```
python manage.py createsuperuser
```

- Запустить проект:

```
python manage.py runserver
```

# Описание

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

http://127.0.0.1:8000/redoc/ Документация для YaMDb

# Системные требования
- Python 3.7+
- Works on Linux, Windows, macOS

# Стек технологий

- Python 3.7

- Django 3.2

- DRF

- JWT + Djoser

# Установка

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Ekaterishe4ka/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект: 

```
python3 manage.py runserver
```

## Примеры запросов к API

Регистрация нового пользователя: 

```
POST /api/v1/auth/signup/
```

Получение данных своей учетной записи:

```
GET /api/v1/users/me/
```


Получение списка всех отзывов:

```
GET /api/v1/titles/{title_id}/reviews/
```

Добавление комментария к отзыву:

```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Добавление новой категории:

```
POST /api/v1/categories/
```

Удаление жанра:

```
DELETE /api/v1/genres/{slug}
```

Частичное обновление информации о произведении:

```
PATCH /api/v1/titles/{titles_id}
```

Полный список запросов API находятся в документации.

## Авторы проекта
```
Наталья https://github.com/Natali7077

Олег https://github.com/tetrapack55

Сергей https://github.com/ir0nc0re
```
