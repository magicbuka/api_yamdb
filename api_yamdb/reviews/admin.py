from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserClass(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role',
        'bio', 'first_name', 'last_name',
        'is_superuser', 'confirmation_code'
    )
    list_filter = ('role',)
    search_fields = ('username', 'email', 'role',)
    empty_value_display = '-empty-'


@admin.register(Category)
class CategoryClass(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Comment)
class CommentClass(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review',)
    list_filter = ('review', 'author', 'pub_date',)
    search_fields = ('review', 'author', 'pub_date',)
    empty_value_display = '-empty-'


@admin.register(Genre)
class GenreClass(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Title)
class TitleClass(admin.ModelAdmin):
    list_display = (
        'name', 'year',
        'category', 'description',
    )
    list_filter = ('genre', 'year', 'category',)
    search_fields = ('genre', 'year', 'category',)
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewClass(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'pub_date',
        'title_id', 'score',
    )
    list_filter = ('author', 'pub_date', 'title_id', 'score',)
    search_fields = ('title', 'author', 'pub_date',)
    empty_value_display = '-empty-'
