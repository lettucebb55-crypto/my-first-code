from django.contrib import admin
from .models import CheckIn, CheckInPhoto


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """打卡记录管理"""
    list_display = ['id', 'user', 'scenic_spot', 'checkin_time', 'is_public', 'created_at']
    list_filter = ['is_public', 'checkin_time', 'created_at']
    search_fields = ['user__username', 'scenic_spot__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'checkin_time'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'scenic_spot', 'checkin_time')
        }),
        ('打卡内容', {
            'fields': ('main_photo', 'notes', 'is_public')
        }),
        ('位置信息', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CheckInPhoto)
class CheckInPhotoAdmin(admin.ModelAdmin):
    """打卡照片管理"""
    list_display = ['id', 'checkin', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['checkin__scenic_spot__name', 'checkin__user__username']
    ordering = ['checkin', 'order']
