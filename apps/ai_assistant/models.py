from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AIQuery(models.Model):
    """
    AI助手查询记录
    保存用户的查询历史和AI生成的规划结果
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                            verbose_name="用户（未登录用户为null）")
    query_type = models.CharField(max_length=20, choices=[
        ('route', '路线规划'),
        ('transport', '交通规划'),
        ('strategy', '旅游策略'),
        ('general', '综合规划'),
    ], default='general', verbose_name="查询类型")
    
    # 用户输入的景点信息
    scenic_spots = models.TextField(verbose_name="景点列表（JSON格式）")
    user_input = models.TextField(verbose_name="用户输入内容")
    
    # AI生成的规划结果
    route_plan = models.TextField(blank=True, null=True, verbose_name="路线规划")
    transport_plan = models.TextField(blank=True, null=True, verbose_name="交通规划")
    strategy_plan = models.TextField(blank=True, null=True, verbose_name="旅游策略")
    full_response = models.TextField(blank=True, null=True, verbose_name="完整AI响应")
    
    # 元数据
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    is_favorite = models.BooleanField(default=False, verbose_name="是否收藏")
    
    class Meta:
        verbose_name = "AI查询记录"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_query_type_display()} - {self.user_input[:50]}"

