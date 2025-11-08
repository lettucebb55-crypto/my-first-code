from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    自定义用户模型
    """
    # 扩展手机号字段，唯一
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    # 扩展头像字段，可设置默认图片
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name="头像")

    # 注册时间 (AbstractUser已包含date_joined)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Favorite(models.Model):
    """
    收藏模型
    """
    TARGET_TYPE_CHOICES = (
        ('scenic', '景点'),
        ('route', '路线'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="用户")
    target_id = models.PositiveIntegerField(verbose_name="收藏目标ID")
    target_type = models.CharField(max_length=10, choices=TARGET_TYPE_CHOICES, verbose_name="收藏类型")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        # 联合约束，避免同一用户重复收藏同一目标
        unique_together = ('user', 'target_id', 'target_type')

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.get_target_type_display()}: {self.target_id}"