from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import Comment


class CommentCreateView(LoginRequiredMixin, View):
    """
    创建评价视图 - 支持景点、路线、酒店等不同类型的评价
    """
    
    def post(self, request):
        """处理评价提交"""
        # 获取参数
        target_type = request.POST.get('target_type')  # scenic, route, hotel
        target_id = request.POST.get('target_id')
        content = request.POST.get('content', '').strip()
        rating = int(request.POST.get('rating', 5))
        
        # 验证参数
        if not all([target_type, target_id, content]):
            messages.error(request, '请填写完整的评价信息')
            return self._redirect_back(request, target_type, target_id)
        
        # 验证评分范围
        if rating < 1 or rating > 5:
            rating = 5
        
        # 验证target_type是否有效
        valid_types = ['scenic', 'route', 'hotel', 'news']
        if target_type not in valid_types:
            messages.error(request, '无效的评价对象类型')
            return self._redirect_back(request, target_type, target_id)
        
        # 检查是否已经评价过（可选：允许重复评价）
        # 这里我们允许用户多次评价，如果需要限制，可以取消下面的注释
        # existing_comment = Comment.objects.filter(
        #     user=request.user,
        #     target_type=target_type,
        #     target_id=target_id,
        #     is_deleted=False
        # ).first()
        # if existing_comment:
        #     messages.warning(request, '您已经评价过该项目了')
        #     return self._redirect_back(request, target_type, target_id)
        
        # 验证目标对象是否存在
        if not self._validate_target(target_type, target_id):
            messages.error(request, '评价对象不存在')
            return self._redirect_back(request, target_type, target_id)
        
        # 创建评价
        try:
            comment = Comment.objects.create(
                user=request.user,
                target_type=target_type,
                target_id=target_id,
                content=content,
                rating=rating
            )
            messages.success(request, '评价提交成功！')
            
            # 如果是AJAX请求，返回JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': '评价提交成功',
                    'comment_id': comment.id
                })
            
        except Exception as e:
            messages.error(request, f'评价提交失败：{str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': f'评价提交失败：{str(e)}'
                })
        
        return self._redirect_back(request, target_type, target_id)
    
    def _validate_target(self, target_type, target_id):
        """验证目标对象是否存在"""
        try:
            if target_type == 'scenic':
                from apps.scenic.models import ScenicSpot
                return ScenicSpot.objects.filter(pk=target_id).exists()
            elif target_type == 'route':
                from apps.routes.models import Route
                return Route.objects.filter(pk=target_id).exists()
            elif target_type == 'hotel':
                from apps.hotels.models import Hotel
                return Hotel.objects.filter(pk=target_id).exists()
            elif target_type == 'news':
                from apps.news.models import News
                return News.objects.filter(pk=target_id).exists()
        except Exception:
            return False
        return False
    
    def _redirect_back(self, request, target_type, target_id):
        """根据target_type重定向到对应的详情页"""
        if target_type == 'scenic':
            from django.urls import reverse
            return redirect(reverse('scenic:detail', kwargs={'pk': target_id}))
        elif target_type == 'route':
            from django.urls import reverse
            return redirect(reverse('routes:detail', kwargs={'pk': target_id}))
        elif target_type == 'hotel':
            from django.urls import reverse
            return redirect(reverse('hotels:detail', kwargs={'pk': target_id}))
        elif target_type == 'news':
            from django.urls import reverse
            return redirect(reverse('news:detail', kwargs={'pk': target_id}))
        else:
            return redirect('/')
