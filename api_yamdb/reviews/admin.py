from django.contrib import admin
# from .models import User, Comment, Review
from .models import Category, Genre, Title


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
#admin.site.register(User)
#admin.site.register(Review)
#admin.site.register(Comment)