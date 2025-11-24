from django.db import models
from django.utils import timezone


class RouteCategory(models.Model):
    """
    路线分类 (按主题或天数)
    """
    name = models.CharField(max_length=50, verbose_name="分类名称")
    description = models.TextField(blank=True, null=True, verbose_name="分类描述")

    class Meta:
        verbose_name = "路线分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Route(models.Model):
    """
    路线核心模型
    """
    category = models.ForeignKey(RouteCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="路线分类")
    name = models.CharField(max_length=100, verbose_name="路线名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    days = models.PositiveIntegerField(default=1, verbose_name="天数")
    group_size = models.PositiveIntegerField(default=10, verbose_name="成团人数")
    deadline = models.DateField(verbose_name="报名截止时间")

    cover_image = models.ImageField(upload_to='route_covers/', verbose_name="封面图")

    # 详情信息
    itinerary_summary = models.TextField(verbose_name="行程概览")
    cost_include = models.TextField(verbose_name="费用包含")
    cost_exclude = models.TextField(verbose_name="费用不含")
    notes = models.TextField(verbose_name="预订须知")

    is_hot = models.BooleanField(default=False, verbose_name="是否热门")
    is_recommended = models.BooleanField(default=False, verbose_name="是否推荐")
    
    # 新增字段：丰富路线信息
    departure_city = models.CharField(max_length=50, default='保定', verbose_name="出发城市")
    meeting_point = models.CharField(max_length=200, blank=True, null=True, verbose_name="集合地点")
    tags = models.CharField(max_length=200, blank=True, null=True, verbose_name="特色标签（用逗号分隔）")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="路线评分")
    views_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="销售数量")
    display_order = models.PositiveIntegerField(default=0, verbose_name="显示顺序（数字越小越靠前）")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "旅游路线"
        verbose_name_plural = verbose_name
        ordering = ['display_order', '-is_hot', '-rating', '-created_at']

    def __str__(self):
        return self.name
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class RouteItinerary(models.Model):
    """
    路线每日行程
    """
    route = models.ForeignKey(Route, related_name='itineraries', on_delete=models.CASCADE, verbose_name="所属路线")
    day_number = models.PositiveIntegerField(verbose_name="第几天")
    title = models.CharField(max_length=200, verbose_name="当日标题")
    description = models.TextField(verbose_name="行程描述 (含景点、餐饮、住宿)")

    class Meta:
        verbose_name = "每日行程"
        verbose_name_plural = verbose_name
        ordering = ['day_number']

    def __str__(self):
        return f"{self.route.name} - Day {self.day_number}"