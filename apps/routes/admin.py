from django.contrib import admin
from .models import RouteCategory, Route, RouteItinerary


@admin.register(RouteCategory)
class RouteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RouteItineraryInline(admin.TabularInline):
    model = RouteItinerary
    extra = 1


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'days', 'rating', 'is_hot', 'is_recommended', 'sales_count', 'display_order')
    list_filter = ('category', 'days', 'is_hot', 'is_recommended', 'departure_city')
    search_fields = ('name', 'tags', 'itinerary_summary')
    list_editable = ('is_hot', 'is_recommended', 'display_order')
    readonly_fields = ('views_count', 'sales_count', 'created_at', 'updated_at')
    inlines = [RouteItineraryInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'category', 'cover_image', 'departure_city', 'meeting_point')
        }),
        ('价格与行程', {
            'fields': ('price', 'days', 'group_size', 'deadline', 'itinerary_summary')
        }),
        ('费用说明', {
            'fields': ('cost_include', 'cost_exclude', 'notes')
        }),
        ('标签与评分', {
            'fields': ('tags', 'rating', 'is_hot', 'is_recommended', 'display_order')
        }),
        ('统计信息', {
            'fields': ('views_count', 'sales_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
