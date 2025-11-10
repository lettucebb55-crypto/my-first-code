from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Favorite

class CustomUserAdmin(UserAdmin):
    # 在后台列表页显示 'phone'
    list_display = ('username', 'email', 'phone', 'is_staff')
    # 允许在后台编辑 'phone' 和 'avatar'
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'avatar')}),
    )

# 注册你的模型
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Favorite)