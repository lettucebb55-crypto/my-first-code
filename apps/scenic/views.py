from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Avg
from .models import ScenicSpot, ScenicCategory
from apps.comments.models import Comment


class ScenicListView(TemplateView):
    template_name = "scenic/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '景点列表 - 保定旅游网'
        
        # 获取所有分类
        context['categories'] = ScenicCategory.objects.all()
        
        # 获取筛选参数
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search', '')
        
        # 获取景点列表
        spots = ScenicSpot.objects.all()
        
        # 按分类筛选
        if category_id:
            spots = spots.filter(category_id=category_id)
        
        # 搜索筛选
        if search_query:
            spots = spots.filter(name__icontains=search_query)
        
        # 排序
        sort_by = self.request.GET.get('sort', 'display_order')
        if sort_by == 'rating':
            spots = spots.order_by('-rating', '-views_count')
        elif sort_by == 'views':
            spots = spots.order_by('-views_count')
        elif sort_by == 'price_asc':
            spots = spots.order_by('ticket_price')
        elif sort_by == 'price_desc':
            spots = spots.order_by('-ticket_price')
        else:
            spots = spots.order_by('display_order', '-is_hot', '-rating', '-views_count')
        
        context['spots'] = spots
        context['selected_category'] = int(category_id) if category_id else None
        context['search_query'] = search_query
        
        return context

class ScenicDetailView(View):
    """景点详情视图 - 支持GET查看和POST提交评价"""
    template_name = "scenic/detail.html"
    
    def get(self, request, pk):
        """显示景点详情"""
        from django.template.response import TemplateResponse
        
        try:
            spot = ScenicSpot.objects.get(pk=pk)
            # 增加浏览次数
            spot.views_count += 1
            spot.save(update_fields=['views_count'])
            
            # 获取景点图片
            spot_images = spot.images.all().order_by('order')
            
            # 获取相关景点（同分类的其他景点）
            related_spots = ScenicSpot.objects.filter(
                category=spot.category
            ).exclude(pk=pk).order_by('-rating', '-views_count')[:4]
            
            # 获取评价列表（排除已删除的）
            comments = Comment.objects.filter(
                target_type='scenic',
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
                'spot': spot,
                'spot_images': spot_images,
                'related_spots': related_spots,
                'comments': comments,
                'avg_rating': avg_rating,
                'page_title': f"{spot.name} - 景点详情 - 保定旅游网"
            }
            
        except ScenicSpot.DoesNotExist:
            context = {
                'spot': None,
                'page_title': "景点不存在 - 保定旅游网"
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
            return redirect('scenic:detail', pk=pk)
        
        if rating < 1 or rating > 5:
            rating = 5
        
        # 验证景点是否存在
        try:
            spot = ScenicSpot.objects.get(pk=pk)
        except ScenicSpot.DoesNotExist:
            messages.error(request, '景点不存在')
            return redirect('scenic:list')
        
        # 创建评价
        try:
            Comment.objects.create(
                user=request.user,
                target_type='scenic',
                target_id=pk,
                content=content,
                rating=rating
            )
            messages.success(request, '评价提交成功！')
        except Exception as e:
            messages.error(request, f'评价提交失败：{str(e)}')
        
        return redirect('scenic:detail', pk=pk)