from django.views.generic import TemplateView
from django.conf import settings
from django.db.models import Q
from apps.scenic.models import ScenicSpot
from apps.routes.models import Route, RouteCategory
from apps.news.models import News
from apps.hotels.models import Hotel
from apps.comments.models import Comment

# 首页视图
class IndexView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '首页 - 保定旅游网'
        context['MEDIA_URL'] = settings.MEDIA_URL
        
        # 获取热门景点（最多8个）
        context['hot_spots'] = ScenicSpot.objects.filter(is_hot=True)[:8]
        
        # 获取推荐景点（如果热门景点不足8个，用推荐景点补充）
        if context['hot_spots'].count() < 8:
            recommended_spots = ScenicSpot.objects.filter(
                is_recommended=True
            ).exclude(id__in=[s.id for s in context['hot_spots']])[:8 - context['hot_spots'].count()]
            context['hot_spots'] = list(context['hot_spots']) + list(recommended_spots)
        
        # 如果还是不足，获取评分最高的景点
        if len(context['hot_spots']) < 8:
            top_rated_spots = ScenicSpot.objects.exclude(
                id__in=[s.id for s in context['hot_spots']]
            ).order_by('-rating', '-views_count')[:8 - len(context['hot_spots'])]
            context['hot_spots'] = list(context['hot_spots']) + list(top_rated_spots)
        
        # 获取特色路线（按分类分组）
        route_categories = RouteCategory.objects.all()
        context['route_categories'] = {}
        
        for category in route_categories:
            # 获取该分类下的热门或推荐路线（最多3个）
            routes = Route.objects.filter(
                category=category
            ).filter(
                is_hot=True
            )[:3]
            
            # 如果热门路线不足，用推荐路线补充
            if routes.count() < 3:
                recommended_routes = Route.objects.filter(
                    category=category,
                    is_recommended=True
                ).exclude(id__in=[r.id for r in routes])[:3 - routes.count()]
                routes = list(routes) + list(recommended_routes)
            
            # 如果还是不足，获取评分最高的路线
            if len(routes) < 3:
                top_routes = Route.objects.filter(
                    category=category
                ).exclude(
                    id__in=[r.id for r in routes]
                ).order_by('-rating', '-sales_count')[:3 - len(routes)]
                routes = list(routes) + list(top_routes)
            
            if routes:
                context['route_categories'][category.name] = routes
        
        # 获取最新资讯（最多5条）
        context['latest_news'] = News.objects.all().order_by('-published_at')[:5]
        
        # 获取推荐酒店（最多6个）
        context['recommended_hotels'] = Hotel.objects.filter(
            is_recommended=True
        ).order_by('-rating', '-views_count', 'display_order')[:6]
        
        # 如果推荐酒店不足6个，用评分最高的酒店补充
        if context['recommended_hotels'].count() < 6:
            top_hotels = Hotel.objects.exclude(
                id__in=[h.id for h in context['recommended_hotels']]
            ).order_by('-rating', '-views_count')[:6 - context['recommended_hotels'].count()]
            context['recommended_hotels'] = list(context['recommended_hotels']) + list(top_hotels)
        
        # 获取最新评论（最多8条，排除已删除的，按评分和创建时间排序）
        context['latest_comments'] = Comment.objects.filter(
            is_deleted=False
        ).select_related('user').order_by('-rating', '-created_at')[:8]
        
        return context


class SearchView(TemplateView):
    """搜索视图 - 搜索景点、路线、酒店、资讯"""
    template_name = "index/search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['page_title'] = f'搜索结果 - 保定旅游网'
        context['search_query'] = query
        
        if query:
            # 搜索景点
            context['scenic_results'] = ScenicSpot.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )[:10]
            
            # 搜索路线
            context['route_results'] = Route.objects.filter(
                Q(name__icontains=query) |
                Q(itinerary_summary__icontains=query)
            )[:10]
            
            # 搜索酒店
            context['hotel_results'] = Hotel.objects.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(brief__icontains=query)
            )[:10]
            
            # 搜索资讯
            context['news_results'] = News.objects.filter(
                Q(title__icontains=query) |
                Q(abstract__icontains=query) |
                Q(content__icontains=query)
            )[:10]
            
            # 统计总数
            context['total_count'] = (
                context['scenic_results'].count() +
                context['route_results'].count() +
                context['hotel_results'].count() +
                context['news_results'].count()
            )
        else:
            context['scenic_results'] = []
            context['route_results'] = []
            context['hotel_results'] = []
            context['news_results'] = []
            context['total_count'] = 0
        
        return context