from django.db import models
from apps.users.models import CustomUser  # 假设已存在


class NewsCategory(models.Model):
    """
    资讯分类
    """
    name = models.CharField(max_length=50, verbose_name="分类名称")

    class Meta:
        verbose_name = "资讯分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(models.Model):
    """
    资讯核心模型
    """
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, verbose_name="分类")
    title = models.CharField(max_length=200, verbose_name="标题")
    abstract = models.CharField(max_length=255, verbose_name="摘要")
    content = models.TextField(verbose_name="正文")
    cover_image = models.ImageField(upload_to='news_covers/', verbose_name="封面图")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    views_count = models.PositiveIntegerField(default=0, verbose_name="阅读量")

    # 假设作者是管理员，可以简单关联，或者设为 nullable
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="作者")

    class Meta:
        verbose_name = "旅游资讯"
        verbose_name_plural = verbose_name
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    """
    资讯评论模型
    """
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE, verbose_name="所属资讯")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="评论用户")
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    class Meta:
        verbose_name = "资讯评论"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} 评论了 {self.news.title}"