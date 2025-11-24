from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Avg
from django.template.response import TemplateResponse
from .models import Route, RouteCategory
from apps.comments.models import Comment


class RouteListView(TemplateView):
    template_name = "routes/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '路线列表 - 保定旅游网'
        
        # 获取所有分类
        context['categories'] = RouteCategory.objects.all()
        
        # 获取筛选参数
        category_id = self.request.GET.get('category')
        days = self.request.GET.get('days')
        search_query = self.request.GET.get('search', '')
        
        # 获取路线列表
        routes = Route.objects.all()
        
        # 按分类筛选
        if category_id:
            routes = routes.filter(category_id=category_id)
        
        # 按天数筛选
        if days:
            routes = routes.filter(days=int(days))
        
        # 搜索筛选
        if search_query:
            routes = routes.filter(name__icontains=search_query)
        
        # 排序
        sort_by = self.request.GET.get('sort', 'display_order')
        if sort_by == 'rating':
            routes = routes.order_by('-rating', '-sales_count')
        elif sort_by == 'price_asc':
            routes = routes.order_by('price')
        elif sort_by == 'price_desc':
            routes = routes.order_by('-price')
        elif sort_by == 'sales':
            routes = routes.order_by('-sales_count')
        else:
            routes = routes.order_by('display_order', '-is_hot', '-rating', '-sales_count')
        
        context['routes'] = routes
        context['selected_category'] = int(category_id) if category_id else None
        context['selected_days'] = int(days) if days else None
        context['search_query'] = search_query
        
        return context

class RouteDetailView(View):
    """路线详情视图 - 支持GET查看和POST提交评价"""
    template_name = "routes/detail.html"
    
    def get(self, request, pk):
        """显示路线详情"""
        try:
            route = Route.objects.get(pk=pk)
            # 增加浏览次数
            route.views_count += 1
            route.save(update_fields=['views_count'])
            
            # 获取行程安排
            itineraries = route.itineraries.all().order_by('day_number')
            
            # 获取相关路线（同分类的其他路线）
            related_routes = Route.objects.filter(
                category=route.category
            ).exclude(pk=pk).order_by('-rating', '-sales_count')[:3]
            
            # 获取评价列表（排除已删除的）
            comments = Comment.objects.filter(
                target_type='route',
                target_id=pk,
                is_deleted=False
            ).select_related('user').order_by('-created_at')[:20]  # 最多显示20条
            
            # 计算平均评分
            if comments.exists():
                avg_rating = comments.aggregate(
                    avg_rating=Avg('rating')
                )['avg_rating'] or 0
            else:
                avg_rating = 0
            
            context = {
                'route': route,
                'itineraries': itineraries,
                'related_routes': related_routes,
                'comments': comments,
                'avg_rating': avg_rating,
                'page_title': f"{route.name} - 路线详情 - 保定旅游网"
            }
            
        except Route.DoesNotExist:
            context = {
                'route': None,
                'page_title': "路线不存在 - 保定旅游网"
            }
        
        return TemplateResponse(request, self.template_name, context)
    
    def post(self, request, pk):
        """处理评价提交"""
        if not request.user.is_authenticated:
            messages.error(request, '请先登录后再发表评价')
            return redirect('users:login')
        
        # 获取评价内容
        content = request.POST.get('content', '').strip()
        rating = int(request.POST.get('rating', 5))
        
        # 验证内容
        if not content:
            messages.error(request, '请输入评价内容')
            return redirect('routes:detail', pk=pk)
        
        if rating < 1 or rating > 5:
            rating = 5
        
        # 验证路线是否存在
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            messages.error(request, '路线不存在')
            return redirect('routes:list')
        
        # 创建评价
        try:
            Comment.objects.create(
                user=request.user,
                target_type='route',
                target_id=pk,
                content=content,
                rating=rating
            )
            messages.success(request, '评价提交成功！')
        except Exception as e:
            messages.error(request, f'评价提交失败：{str(e)}')
        
        return redirect('routes:detail', pk=pk)