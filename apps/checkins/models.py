from django.db import models
from django.utils import timezone
from apps.users.models import CustomUser
from apps.scenic.models import ScenicSpot


class CheckIn(models.Model):
    """
    旅游打卡签到模型
    记录用户到景点打卡的信息，包括打卡时间、照片、位置等
    """
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='checkins',
        verbose_name="用户"
    )
    scenic_spot = models.ForeignKey(
        ScenicSpot, 
        on_delete=models.CASCADE, 
        related_name='checkins',
        verbose_name="景点"
    )
    
    # 打卡时间
    checkin_time = models.DateTimeField(
        default=timezone.now, 
        verbose_name="打卡时间"
    )
    
    # 打卡照片（支持多张照片，通过CheckInPhoto模型关联）
    # 主照片用于列表展示
    main_photo = models.ImageField(
        upload_to='checkin_photos/', 
        blank=True, 
        null=True,
        verbose_name="主照片"
    )
    
    # 打卡位置（实际打卡时的经纬度，可能与景点位置不同）
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        blank=True, 
        null=True,
        verbose_name="打卡纬度"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        blank=True, 
        null=True,
        verbose_name="打卡经度"
    )
    
    # 备注信息
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name="打卡备注"
    )
    
    # 是否公开（默认公开，用户可以选择是否在个人地图中显示）
    is_public = models.BooleanField(
        default=True,
        verbose_name="是否公开"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间"
    )
    
    class Meta:
        verbose_name = "打卡记录"
        verbose_name_plural = verbose_name
        ordering = ['-checkin_time']
        # 同一用户在同一景点可以多次打卡（不同时间）
        # 但同一天同一景点只允许打卡一次（可选限制，这里不限制）
        indexes = [
            models.Index(fields=['user', '-checkin_time']),
            models.Index(fields=['scenic_spot', '-checkin_time']),
        ]
    
    def __str__(self):
        return f"{self.user.username} 在 {self.scenic_spot.name} 打卡"


class CheckInPhoto(models.Model):
    """
    打卡照片模型
    支持一个打卡记录关联多张照片
    """
    checkin = models.ForeignKey(
        CheckIn, 
        on_delete=models.CASCADE, 
        related_name='photos',
        verbose_name="打卡记录"
    )
    photo = models.ImageField(
        upload_to='checkin_photos/', 
        verbose_name="照片"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="排序"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="上传时间"
    )
    
    class Meta:
        verbose_name = "打卡照片"
        verbose_name_plural = verbose_name
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.checkin.scenic_spot.name} - 照片 {self.order}"
