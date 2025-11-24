from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, RoomType


class RoomTypeInline(admin.TabularInline):
    """房间类型内联编辑"""
    model = RoomType
    extra = 1
    fields = ('name', 'price', 'capacity', 'remaining_count', 'is_available', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """酒店管理 - 支持完整的增删改查"""
    list_display = ('name', 'address', 'phone', 'rating', 'is_recommended', 'views_count', 'display_order', 'created_at')
    list_filter = ('is_recommended', 'created_at', 'rating')
    search_fields = ('name', 'address', 'phone', 'brief', 'description')
    list_editable = ('is_recommended', 'display_order')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'cover_image_preview')
    inlines = [RoomTypeInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'address', 'phone', 'cover_image', 'cover_image_preview')
        }),
        ('介绍信息', {
            'fields': ('brief', 'description')
        }),
        ('位置信息', {
            'fields': ('latitude', 'longitude')
        }),
        ('推荐与排序', {
            'fields': ('is_recommended', 'rating', 'display_order')
        }),
        ('统计信息', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_image_preview(self, obj):
        """显示封面图预览"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.cover_image.url
            )
        return "无封面图"
    cover_image_preview.short_description = "封面图预览"


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """房间类型管理 - 支持完整的增删改查"""
    list_display = ('name', 'hotel', 'price', 'capacity', 'remaining_count', 'is_available', 'created_at')
    list_filter = ('hotel', 'is_available', 'capacity', 'created_at')
    search_fields = ('name', 'hotel__name', 'description')
    list_editable = ('is_available', 'remaining_count')
    readonly_fields = ('created_at', 'updated_at', 'cover_image_preview')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('hotel', 'name', 'cover_image', 'cover_image_preview')
        }),
        ('价格与容量', {
            'fields': ('price', 'capacity', 'remaining_count', 'is_available')
        }),
        ('房间描述', {
            'fields': ('description',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_image_preview(self, obj):
        """显示房间图片预览"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.cover_image.url
            )
        return "无图片"
    cover_image_preview.short_description = "房间图片预览"
