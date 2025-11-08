from django.db import models
from apps.users.models import CustomUser


class Order(models.Model):
    """
    订单核心模型
    """
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    order_sn = models.CharField(max_length=50, unique=True, verbose_name="订单编号")
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="下单用户")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="订单总金额")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")

    contact_name = models.CharField(max_length=50, verbose_name="联系人姓名")
    contact_phone = models.CharField(max_length=11, verbose_name="联系人手机")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_sn


class OrderDetail(models.Model):
    """
    订单明细
    """
    ITEM_TYPE_CHOICES = (
        ('scenic', '景点门票'),
        ('route', '路线报名'),
    )

    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE, verbose_name="所属订单")
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, verbose_name="项目类型")
    item_id = models.PositiveIntegerField(verbose_name="项目ID")

    # 冗余存储，避免关联数据变更
    item_name = models.CharField(max_length=100, verbose_name="项目名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="小计")

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.order.order_sn} - {self.item_name}"