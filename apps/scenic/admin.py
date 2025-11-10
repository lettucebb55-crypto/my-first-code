from django.contrib import admin
from .models import ScenicCategory, ScenicSpot, ScenicImage

# 允许在添加景点时，直接上传多张图片 (内联)
class ScenicImageInline(admin.TabularInline):
    model = ScenicImage
    extra = 1 # 默认显示1个额外的上传框

@admin.register(ScenicSpot)
class ScenicSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ticket_price', 'is_hot', 'is_recommended')
    list_filter = ('category', 'is_hot', 'is_recommended') # 添加右侧过滤器
    search_fields = ('name', 'address') # 添加搜索框
    inlines = [ScenicImageInline] # 挂载图片内联

admin.site.register(ScenicCategory)