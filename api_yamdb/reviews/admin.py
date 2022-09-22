from django.contrib import admin

from .models import User, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('role',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date', 'text',)
    search_fields = ('review', 'author','text',)
    list_filter = ('review', 'author',)


admin.site.register(User, PostAdmin)
admin.site.register(Comment, CommentAdmin)
