from django.db import models


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

    class Meta:
        verbose_name = "旅游路线"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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