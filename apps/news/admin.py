from django.contrib import admin
from .models import NewsCategory, News, NewsComment


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'views_count')
    list_filter = ('category', 'author', 'published_at')
    search_fields = ('title', 'content')


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
