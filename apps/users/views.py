from django.views.generic import TemplateView, CreateView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin  # 导入登录验证
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views import View
from apps.orders.models import Order  # 导入订单模型
from apps.comments.models import Comment  # 导入评论模型
from .forms import CustomUserCreationForm


# 简单的视图骨架，后续填充逻辑
class UserHomeView(LoginRequiredMixin, TemplateView):  # 添加 LoginRequiredMixin
    template_name = "user/home.html"

    # 获取订单数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 获取最近3条订单
        context['recent_orders'] = Order.objects.filter(user=user).order_by('-created_at')[:3]
        
        # 统计数据
        # 1. 总订单数
        context['total_orders'] = Order.objects.filter(user=user).count()
        
        # 2. 我的收藏数
        from .models import Favorite
        context['total_favorites'] = Favorite.objects.filter(user=user).count()
        
        # 3. 已发评价数（排除已删除的）
        from apps.comments.models import Comment
        context['total_comments'] = Comment.objects.filter(
            user=user,
            is_deleted=False
        ).count()
        
        return context


class UserProfileView(LoginRequiredMixin, TemplateView):  # 添加 LoginRequiredMixin
    template_name = "user/profile.html"
    # 需要用户登录


class UserOrdersView(LoginRequiredMixin, TemplateView):  # 添加 LoginRequiredMixin
    template_name = "user/orders.html"

    # 获取订单数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前用户的所有订单
        orders = Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('details')
        
        # 按状态筛选
        status = self.request.GET.get('status', '')
        if status:
            orders = orders.filter(status=status)
        
        context['orders'] = orders
        context['selected_status'] = status
        return context


class UserFavoritesView(LoginRequiredMixin, TemplateView):  # 添加 LoginRequiredMixin
    template_name = "user/favorites.html"
    # 需要用户登录
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Favorite
        
        # 获取当前用户的所有收藏
        favorites = Favorite.objects.filter(user=self.request.user).order_by('-created_at')
        
        # 为每个收藏获取对应的对象信息
        favorite_list = []
        for favorite in favorites:
            favorite_data = {
                'favorite': favorite,
                'target_name': '未知',
                'target_image': None,
                'target_url': '#',
                'target_type_display': favorite.get_target_type_display(),
            }
            
            # 根据target_type获取对应的对象信息
            if favorite.target_type == 'scenic':
                try:
                    from apps.scenic.models import ScenicSpot
                    target = ScenicSpot.objects.get(pk=favorite.target_id)
                    favorite_data['target_name'] = target.name
                    favorite_data['target_image'] = target.cover_image.url if target.cover_image else None
                    favorite_data['target_url'] = f'/scenic/detail/{target.id}/'
                except:
                    favorite_data['target_name'] = f'景点 #{favorite.target_id} (已删除)'
            elif favorite.target_type == 'route':
                try:
                    from apps.routes.models import Route
                    target = Route.objects.get(pk=favorite.target_id)
                    favorite_data['target_name'] = target.name
                    favorite_data['target_image'] = target.cover_image.url if target.cover_image else None
                    favorite_data['target_url'] = f'/routes/detail/{target.id}/'
                except:
                    favorite_data['target_name'] = f'路线 #{favorite.target_id} (已删除)'
            else:
                # 处理其他类型（如未来可能添加的酒店等）
                favorite_data['target_name'] = f'{favorite.get_target_type_display()} #{favorite.target_id}'
            
            favorite_list.append(favorite_data)
        
        context['favorite_list'] = favorite_list
        return context


class UserReviewsView(LoginRequiredMixin, TemplateView):  # 添加 LoginRequiredMixin
    template_name = "user/reviews.html"
    # 需要用户登录
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前用户的所有评论（排除已删除的）
        comments = Comment.objects.filter(
            user=self.request.user,
            is_deleted=False
        ).order_by('-created_at')
        
        # 为每个评论获取关联的对象信息
        comment_list = []
        for comment in comments:
            comment_data = {
                'comment': comment,
                'target_name': '未知',
                'target_id': comment.target_id,
                'target_type': comment.target_type,
            }
            
            # 根据target_type获取对应的对象名称
            if comment.target_type == 'scenic':
                try:
                    from apps.scenic.models import ScenicSpot
                    target = ScenicSpot.objects.get(pk=comment.target_id)
                    comment_data['target_name'] = target.name
                except:
                    pass
            elif comment.target_type == 'route':
                try:
                    from apps.routes.models import Route
                    target = Route.objects.get(pk=comment.target_id)
                    comment_data['target_name'] = target.name
                except:
                    pass
            elif comment.target_type == 'hotel':
                try:
                    from apps.hotels.models import Hotel
                    target = Hotel.objects.get(pk=comment.target_id)
                    comment_data['target_name'] = target.name
                except:
                    pass
            elif comment.target_type == 'news':
                try:
                    from apps.news.models import News
                    target = News.objects.get(pk=comment.target_id)
                    comment_data['target_name'] = target.title
                except:
                    pass
            
            comment_list.append(comment_data)
        
        context['comment_list'] = comment_list
        return context


class LoginView(DjangoLoginView):
    """登录视图"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # 如果已登录，重定向到首页
    
    def form_valid(self, form):
        """处理登录表单验证成功"""
        # 先获取用户（在登录之前）
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            # 登录用户
            login(self.request, user)
            
            # 如果用户是管理员（staff或superuser），重定向到管理员后台
            if user.is_staff or user.is_superuser:
                from django.http import HttpResponseRedirect
                # next 可来自 GET 或 POST（隐藏域）
                next_url = self.request.GET.get('next') or self.request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect('/admin_panel/')
        
        # 调用父类方法处理重定向（普通用户）
        return super().form_valid(form)
    
    def get_success_url(self):
        """登录成功后重定向"""
        # 如果URL中有next参数，优先使用
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        
        # 默认重定向到首页
        return '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '登录 - 保定旅游网'
        return context


class RegisterView(CreateView):
    """注册视图"""
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '注册 - 保定旅游网'
        return context
    
    def form_valid(self, form):
        """注册成功后自动登录"""
        response = super().form_valid(form)
        # 自动登录新注册的用户
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return response


class LogoutView(View):
    """退出登录视图 - 支持GET请求"""
    def get(self, request):
        """处理GET请求退出登录"""
        logout(request)
        return HttpResponseRedirect('/')
    
    def post(self, request):
        """处理POST请求退出登录"""
        logout(request)
        return HttpResponseRedirect('/')