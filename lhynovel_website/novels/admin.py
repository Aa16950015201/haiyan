from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Genre, Book, Chapter, Comment, UserBook

# 注册模型到 Django admin
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(UserBook)