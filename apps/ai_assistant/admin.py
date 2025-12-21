from django.contrib import admin
from .models import AIQuery


@admin.register(AIQuery)
class AIQueryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'query_type', 'user_input', 'created_at', 'is_favorite']
    list_filter = ['query_type', 'is_favorite', 'created_at']
    search_fields = ['user_input', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

