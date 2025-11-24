from django.contrib import admin
from django.utils.html import format_html
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """评论管理 - 支持完整的增删改查"""
    list_display = ('id', 'user', 'target_type', 'target_id', 'rating', 'rating_stars', 'is_deleted', 'created_at')
    list_filter = ('target_type', 'rating', 'is_deleted', 'created_at')
    search_fields = ('user__username', 'user__email', 'content', 'target_id')
    list_editable = ('is_deleted',)
    readonly_fields = ('created_at', 'updated_at', 'images_preview')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('评论信息', {
            'fields': ('user', 'target_type', 'target_id', 'content', 'rating')
        }),
        ('图片信息', {
            'fields': ('images', 'images_preview'),
            'classes': ('collapse',)
        }),
        ('状态信息', {
            'fields': ('is_deleted', 'created_at', 'updated_at')
        }),
    )
    
    def rating_stars(self, obj):
        """显示评分星星"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        colors = {
            5: '#10b981',
            4: '#3b82f6',
            3: '#f59e0b',
            2: '#ef4444',
            1: '#dc2626',
        }
        color = colors.get(obj.rating, '#6b7280')
        return format_html(
            '<span style="color: {}; font-size: 16px;">{}</span>',
            color,
            stars
        )
    rating_stars.short_description = "评分"
    
    def images_preview(self, obj):
        """显示评论图片预览"""
        images = obj.get_images_list()
        if images:
            html = '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
            for img_path in images[:5]:  # 最多显示5张
                html += format_html(
                    '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;" />',
                    img_path
                )
            html += '</div>'
            return format_html(html)
        return "无图片"
    images_preview.short_description = "评论图片"
    
    actions = ['mark_as_deleted', 'mark_as_undeleted']
    
    def mark_as_deleted(self, request, queryset):
        """批量标记为已删除"""
        count = queryset.update(is_deleted=True)
        self.message_user(request, f"已将 {count} 条评论标记为已删除")
    mark_as_deleted.short_description = "标记为已删除"
    
    def mark_as_undeleted(self, request, queryset):
        """批量标记为未删除"""
        count = queryset.update(is_deleted=False)
        self.message_user(request, f"已将 {count} 条评论标记为未删除")
    mark_as_undeleted.short_description = "标记为未删除"
