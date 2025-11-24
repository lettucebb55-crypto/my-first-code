from django.contrib import admin
from .models import ScenicCategory, ScenicSpot, ScenicImage


@admin.register(ScenicCategory)
class ScenicCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ScenicImageInline(admin.TabularInline):
    model = ScenicImage
    extra = 1


@admin.register(ScenicSpot)
class ScenicSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ticket_price', 'rating', 'is_hot', 'is_recommended', 'views_count', 'display_order')
    list_filter = ('category', 'is_hot', 'is_recommended', 'best_season')
    search_fields = ('name', 'address', 'tags', 'description')
    list_editable = ('is_hot', 'is_recommended', 'display_order')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [ScenicImageInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'category', 'cover_image', 'description')
        }),
        ('详细信息', {
            'fields': ('address', 'ticket_price', 'open_time', 'phone', 'traffic_info', 
                      'best_season', 'visit_duration', 'latitude', 'longitude')
        }),
        ('标签与评分', {
            'fields': ('tags', 'rating', 'is_hot', 'is_recommended', 'display_order')
        }),
        ('统计信息', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
