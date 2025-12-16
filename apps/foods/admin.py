from django.contrib import admin
from .models import FoodCategory, Food, FoodImage


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    """美食分类管理"""
    list_display = ['name', 'display_order', 'icon']
    list_filter = ['display_order']
    search_fields = ['name', 'description']
    ordering = ['display_order', 'name']


class FoodImageInline(admin.TabularInline):
    """美食图片内联编辑"""
    model = FoodImage
    extra = 1
    fields = ['image', 'description', 'order']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    """美食管理"""
    list_display = ['name', 'category', 'is_hot', 'is_recommended', 'is_traditional', 'rating', 'views_count', 'created_at']
    list_filter = ['category', 'is_hot', 'is_recommended', 'is_traditional', 'created_at']
    search_fields = ['name', 'english_name', 'description', 'ingredients', 'tags']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [FoodImageInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('category', 'name', 'english_name', 'cover_image')
        }),
        ('详细介绍', {
            'fields': ('description', 'ingredients', 'cooking_method', 'cultural_background')
        }),
        ('价格信息', {
            'fields': ('price_range', 'average_price'),
            'classes': ('collapse',)
        }),
        ('推荐设置', {
            'fields': ('is_recommended', 'is_hot', 'is_traditional', 'rating')
        }),
        ('其他信息', {
            'fields': ('tags', 'recommended_restaurants', 'display_order', 'views_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    """美食图片管理"""
    list_display = ['food', 'order', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['food__name', 'description']
    ordering = ['food', 'order']
