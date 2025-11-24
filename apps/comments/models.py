from django.db import models
from django.utils import timezone
from apps.users.models import CustomUser


class Comment(models.Model):
    """
    评论模型 - 通用评论系统，可用于景点、路线、酒店、资讯等
    """
    CONTENT_TYPE_CHOICES = [
        ('scenic', '景点'),
        ('route', '路线'),
        ('hotel', '酒店'),
        ('news', '资讯'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="评论用户")
    target_id = models.PositiveIntegerField(verbose_name="关联对象ID")
    target_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, verbose_name="关联对象类型")
    content = models.TextField(verbose_name="评论内容")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5, verbose_name="评分（1-5分）")
    images = models.TextField(blank=True, null=True, verbose_name="评论图片（多个图片路径用逗号分隔）")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} 评论了 {self.get_target_type_display()} #{self.target_id}"
    
    def get_images_list(self):
        """获取图片列表"""
        if self.images:
            return [img.strip() for img in self.images.split(',') if img.strip()]
        return []
