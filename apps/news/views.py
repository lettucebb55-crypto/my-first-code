from django.views.generic import TemplateView
from .models import News, NewsCategory


class NewsListView(TemplateView):
    template_name = "news/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '旅游资讯 - 保定旅游网'
        
        # 获取所有分类
        context['categories'] = NewsCategory.objects.all()
        
        # 获取筛选参数
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search', '')
        
        # 获取资讯列表
        news_list = News.objects.all()
        
        # 按分类筛选
        if category_id:
            news_list = news_list.filter(category_id=category_id)
        
        # 搜索筛选
        if search_query:
            news_list = news_list.filter(title__icontains=search_query)
        
        # 按发布时间排序
        news_list = news_list.order_by('-published_at')
        
        context['news_list'] = news_list
        context['selected_category'] = int(category_id) if category_id else None
        context['search_query'] = search_query
        
        return context

class NewsDetailView(TemplateView):
    template_name = "news/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        
        try:
            news = News.objects.get(pk=pk)
            # 增加浏览次数
            news.views_count += 1
            news.save(update_fields=['views_count'])
            
            context['news'] = news
            context['page_title'] = f"{news.title} - 保定旅游网"
            
            # 获取相关资讯（同分类的其他资讯）
            related_news = News.objects.filter(
                category=news.category
            ).exclude(pk=pk).order_by('-published_at')[:3]
            context['related_news'] = related_news
            
            # 获取评论
            context['comments'] = news.comments.all().order_by('-created_at')[:10]
            
        except News.DoesNotExist:
            context['news'] = None
            context['page_title'] = "资讯不存在 - 保定旅游网"
        
        return context