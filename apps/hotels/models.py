from django.db import models
from django.utils import timezone


class Hotel(models.Model):
    """
    酒店核心模型
    """
    name = models.CharField(max_length=100, verbose_name="酒店名称")
    address = models.CharField(max_length=255, verbose_name="详细地址")
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    brief = models.CharField(max_length=255, verbose_name="简介")
    description = models.TextField(verbose_name="详情介绍")
    is_recommended = models.BooleanField(default=False, verbose_name="是否推荐")
    cover_image = models.ImageField(upload_to='hotel_covers/', blank=True, null=True, verbose_name="封面图")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    # 扩展字段
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="评分")
    views_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="纬度")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="经度")
    display_order = models.PositiveIntegerField(default=0, verbose_name="显示顺序（数字越小越靠前）")
    
    class Meta:
        verbose_name = "酒店"
        verbose_name_plural = verbose_name
        ordering = ['display_order', '-is_recommended', '-rating', '-created_at']
    
    def __str__(self):
        return self.name


class RoomType(models.Model):
    """
    房间类型模型
    """
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE, verbose_name="所属酒店")
    name = models.CharField(max_length=100, verbose_name="房型名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    capacity = models.PositiveIntegerField(verbose_name="容纳人数")
    description = models.TextField(verbose_name="房间描述")
    remaining_count = models.PositiveIntegerField(default=0, verbose_name="剩余数量")
    is_available = models.BooleanField(default=True, verbose_name="是否可预订")
    cover_image = models.ImageField(upload_to='room_covers/', blank=True, null=True, verbose_name="房间图片")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "房间类型"
        verbose_name_plural = verbose_name
        ordering = ['hotel', 'price', '-created_at']
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"
