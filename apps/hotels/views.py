from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Avg
from django.template.response import TemplateResponse
from .models import Hotel
from apps.comments.models import Comment


class HotelListView(TemplateView):
    """酒店列表视图"""
    template_name = "hotels/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '推荐酒店 - 保定旅游网'
        
        # 获取筛选参数
        search_query = self.request.GET.get('search', '')
        is_recommended = self.request.GET.get('recommended')
        
        # 获取酒店列表
        hotels = Hotel.objects.all()
        
        # 按推荐筛选
        if is_recommended == '1':
            hotels = hotels.filter(is_recommended=True)
        
        # 搜索筛选
        if search_query:
            hotels = hotels.filter(name__icontains=search_query)
        
        # 排序
        sort_by = self.request.GET.get('sort', 'display_order')
        if sort_by == 'rating':
            hotels = hotels.order_by('-rating', '-views_count')
        elif sort_by == 'views':
            hotels = hotels.order_by('-views_count')
        elif sort_by == 'price_asc':
            hotels = hotels.order_by('room_types__price')
        elif sort_by == 'price_desc':
            hotels = hotels.order_by('-room_types__price')
        else:
            hotels = hotels.order_by('display_order', '-is_recommended', '-rating', '-views_count')
        
        context['hotels'] = hotels
        context['search_query'] = search_query
        context['is_recommended'] = is_recommended == '1'
        
        return context


class HotelDetailView(View):
    """酒店详情视图 - 支持GET查看和POST提交评价"""
    template_name = "hotels/detail.html"
    
    def get(self, request, pk):
        """显示酒店详情"""
        try:
            hotel = Hotel.objects.get(pk=pk)
            # 增加浏览次数
            hotel.views_count += 1
            hotel.save(update_fields=['views_count'])
            
            # 获取房间类型
            room_types = hotel.room_types.filter(is_available=True).order_by('price')
            
            # 获取相关酒店（推荐的其他酒店）
            related_hotels = Hotel.objects.filter(
                is_recommended=True
            ).exclude(pk=pk).order_by('-rating', '-views_count')[:4]
            
            # 获取评价列表（排除已删除的）
            comments = Comment.objects.filter(
                target_type='hotel',
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
                'hotel': hotel,
                'room_types': room_types,
                'related_hotels': related_hotels,
                'comments': comments,
                'avg_rating': avg_rating,
                'page_title': f"{hotel.name} - 酒店详情 - 保定旅游网"
            }
            
        except Hotel.DoesNotExist:
            context = {
                'hotel': None,
                'page_title': "酒店不存在 - 保定旅游网"
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
            return redirect('hotels:detail', pk=pk)
        
        if rating < 1 or rating > 5:
            rating = 5
        
        # 验证酒店是否存在
        try:
            hotel = Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            messages.error(request, '酒店不存在')
            return redirect('hotels:list')
        
        # 创建评价
        try:
            Comment.objects.create(
                user=request.user,
                target_type='hotel',
                target_id=pk,
                content=content,
                rating=rating
            )
            messages.success(request, '评价提交成功！')
        except Exception as e:
            messages.error(request, f'评价提交失败：{str(e)}')
        
        return redirect('hotels:detail', pk=pk)
