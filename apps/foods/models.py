from django.db import models
from django.utils import timezone


class FoodCategory(models.Model):
    """
    美食分类
    """
    name = models.CharField(max_length=50, verbose_name="分类名称")
    description = models.TextField(blank=True, null=True, verbose_name="分类描述")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="图标类名（Font Awesome）")
    display_order = models.PositiveIntegerField(default=0, verbose_name="显示顺序")

    class Meta:
        verbose_name = "美食分类"
        verbose_name_plural = verbose_name
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Food(models.Model):
    """
    美食核心模型
    """
    category = models.ForeignKey(
        FoodCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='foods',
        verbose_name="美食分类"
    )
    name = models.CharField(max_length=100, verbose_name="美食名称")
    english_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="英文名称")
    
    # 基本信息
    description = models.TextField(verbose_name="美食介绍")
    ingredients = models.TextField(blank=True, null=True, verbose_name="主要食材")
    cooking_method = models.TextField(blank=True, null=True, verbose_name="制作方法")
    cultural_background = models.TextField(blank=True, null=True, verbose_name="文化背景")
    
    # 图片
    cover_image = models.ImageField(upload_to='food_covers/', verbose_name="封面图")
    
    # 价格信息（可选，有些美食可能不标价）
    price_range = models.CharField(max_length=50, blank=True, null=True, verbose_name="价格区间")
    average_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="平均价格")
    
    # 推荐信息
    is_recommended = models.BooleanField(default=False, verbose_name="是否推荐")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门")
    is_traditional = models.BooleanField(default=False, verbose_name="是否传统美食")
    
    # 评分和统计
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="评分")
    views_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    
    # 标签
    tags = models.CharField(max_length=200, blank=True, null=True, verbose_name="标签（用逗号分隔）")
    
    # 推荐餐厅（可选）
    recommended_restaurants = models.TextField(blank=True, null=True, verbose_name="推荐餐厅（用换行分隔）")
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    display_order = models.PositiveIntegerField(default=0, verbose_name="显示顺序")

    class Meta:
        verbose_name = "美食"
        verbose_name_plural = verbose_name
        ordering = ['display_order', '-is_hot', '-is_recommended', '-rating', '-created_at']
        indexes = [
            models.Index(fields=['category', '-is_hot', '-rating']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_restaurants_list(self):
        """获取推荐餐厅列表"""
        if self.recommended_restaurants:
            return [r.strip() for r in self.recommended_restaurants.split('\n') if r.strip()]
        return []


class FoodImage(models.Model):
    """
    美食图片
    """
    food = models.ForeignKey(
        Food, 
        related_name='images', 
        on_delete=models.CASCADE, 
        verbose_name="所属美食"
    )
    image = models.ImageField(upload_to='food_images/', verbose_name="图片")
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="图片描述")
    order = models.PositiveIntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        verbose_name = "美食图片"
        verbose_name_plural = verbose_name
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.food.name} - 图片 {self.order}"
