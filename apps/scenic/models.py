from django.db import models


class ScenicCategory(models.Model):
    """
    景点分类
    """
    name = models.CharField(max_length=50, verbose_name="分类名称")
    description = models.TextField(blank=True, null=True, verbose_name="分类描述")

    class Meta:
        verbose_name = "景点分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ScenicSpot(models.Model):
    """
    景点核心模型
    """
    category = models.ForeignKey(ScenicCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="景点分类")
    name = models.CharField(max_length=100, verbose_name="景点名称")
    address = models.CharField(max_length=255, verbose_name="详细地址")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="门票价格")
    open_time = models.CharField(max_length=100, verbose_name="开放时间")
    description = models.TextField(verbose_name="详细介绍")
    cover_image = models.ImageField(upload_to='scenic_covers/', verbose_name="封面图")

    is_hot = models.BooleanField(default=False, verbose_name="是否热门")
    is_recommended = models.BooleanField(default=False, verbose_name="是否推荐")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 评分字段
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="评分")
    
    # 新增字段：丰富景点信息
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="联系电话")
    traffic_info = models.TextField(blank=True, null=True, verbose_name="交通信息")
    best_season = models.CharField(max_length=50, blank=True, null=True, verbose_name="最佳游览季节")
    visit_duration = models.CharField(max_length=50, blank=True, null=True, verbose_name="建议游览时长")
    tags = models.CharField(max_length=200, blank=True, null=True, verbose_name="标签（用逗号分隔）")
    views_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="纬度")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="经度")
    display_order = models.PositiveIntegerField(default=0, verbose_name="显示顺序（数字越小越靠前）")

    class Meta:
        verbose_name = "景点"
        verbose_name_plural = verbose_name
        ordering = ['display_order', '-is_hot', '-rating', '-created_at']

    def __str__(self):
        return self.name
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class ScenicImage(models.Model):
    """
    景点图片
    """
    spot = models.ForeignKey(ScenicSpot, related_name='images', on_delete=models.CASCADE, verbose_name="所属景点")
    image = models.ImageField(upload_to='scenic_images/', verbose_name="图片")
    order = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "景点图片"
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return f"{self.spot.name} - 图片 {self.order}"