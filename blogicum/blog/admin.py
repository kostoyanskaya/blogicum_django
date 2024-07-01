from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at',)
    list_filter = ('is_published',)
    search_fields = ('title', 'description',)


@admin.register(Location)
class Locationadmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at',)
    list_filter = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'pub_date', 'is_published',)
    list_filter = ('category', 'is_published',)
    search_fields = ('title', 'text',)
