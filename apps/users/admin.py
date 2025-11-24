from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Favorite


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """自定义用户管理 - 支持完整的增删改查"""
    list_display = ('username', 'email', 'phone', 'avatar_preview', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'phone', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    list_editable = ('is_active', 'is_staff')
    readonly_fields = ('date_joined', 'last_login', 'avatar_preview')
    ordering = ('-date_joined',)
    
    # 添加自定义字段到fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('phone', 'avatar', 'avatar_preview')}),
    )
    
    # 添加自定义字段到add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('额外信息', {'fields': ('phone', 'avatar')}),
    )
    
    def avatar_preview(self, obj):
        """显示头像预览"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.avatar.url
            )
        return "无头像"
    avatar_preview.short_description = "头像预览"
    
    # 批量操作
    actions = ['make_active', 'make_inactive', 'make_staff', 'remove_staff']
    
    def make_active(self, request, queryset):
        """批量激活用户"""
        queryset.update(is_active=True)
        self.message_user(request, f"已激活 {queryset.count()} 个用户")
    make_active.short_description = "激活选中的用户"
    
    def make_inactive(self, request, queryset):
        """批量停用用户"""
        queryset.update(is_active=False)
        self.message_user(request, f"已停用 {queryset.count()} 个用户")
    make_inactive.short_description = "停用选中的用户"
    
    def make_staff(self, request, queryset):
        """批量设置为员工"""
        queryset.update(is_staff=True)
        self.message_user(request, f"已将 {queryset.count()} 个用户设置为员工")
    make_staff.short_description = "设置为员工"
    
    def remove_staff(self, request, queryset):
        """批量移除员工权限"""
        queryset.update(is_staff=False)
        self.message_user(request, f"已移除 {queryset.count()} 个用户的员工权限")
    remove_staff.short_description = "移除员工权限"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """收藏管理 - 支持完整的增删改查"""
    list_display = ('id', 'user', 'target_type', 'target_id', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('target_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__phone', 'target_id')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # 允许在列表页直接编辑
    list_editable = ('target_type',)
    
    # 详情页字段分组
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'target_type', 'target_id')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
