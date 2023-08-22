from django.contrib import admin

from .models import (
    User, Subscribe
)

EMPTY_VALUE = '-empty-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User Administration Model"""
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display_links = ('username', )
    # empty_value_display = EMPTY_VALUE


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Subscribe Administration Model"""
    list_display = (
        'id',
        'user',
        'author',
    )
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    list_display = ('user', 'author')
    # empty_value_display = EMPTY_VALUE
