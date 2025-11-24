from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy

# 导入所有需要的模型
from apps.users.models import CustomUser
from apps.orders.models import Order, OrderDetail
from apps.scenic.models import ScenicSpot, ScenicCategory
from apps.routes.models import Route, RouteCategory
from apps.hotels.models import Hotel
from apps.news.models import News, NewsCategory
from apps.comments.models import Comment

# 导入表单
from .forms import ScenicSpotForm, RouteForm, HotelForm, NewsForm, UserForm, OrderStatusForm


# 添加权限验证，确保只有职员(staff)才能访问
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # 仅当用户是 "staff" (职员) 时才允许访问
        return self.request.user.is_staff


class AdminIndexView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/dashboard.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '数据概览'

        # 1. 基础数据统计
        context['total_users'] = CustomUser.objects.count()
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='pending').count()
        context['total_scenic'] = ScenicSpot.objects.count()
        context['total_routes'] = Route.objects.count()
        context['total_hotels'] = Hotel.objects.count()
        context['total_news'] = News.objects.count()

        # 今日预订
        today = timezone.now().date()
        context['today_orders'] = Order.objects.filter(created_at__date=today).count()

        # 总收入统计
        context['total_revenue'] = Order.objects.filter(status__in=['paid', 'completed']).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # 2. 热门排行
        top_spots = OrderDetail.objects.filter(item_type='scenic') \
            .values('item_name') \
            .annotate(order_count=Count('id')) \
            .order_by('-order_count')[:5]

        top_routes = OrderDetail.objects.filter(item_type='route') \
            .values('item_name') \
            .annotate(order_count=Count('id')) \
            .order_by('-order_count')[:5]

        context['top_spots'] = top_spots
        context['top_routes'] = top_routes

        return context


class ScenicListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/scenic_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = ScenicSpot.objects.select_related('category').all().order_by('-created_at')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(description__icontains=search)
            )

        category_id = self.request.GET.get('category', '')
        if category_id:
            query = query.filter(category_id=category_id)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': ScenicCategory.objects.all(),
            'search': search,
            'category_id': category_id,
            'per_page': per_page,
        })
        return context


class RoutesListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/routes_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Route.objects.select_related('category').all().order_by('-created_at')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(name__icontains=search) |
                Q(itinerary_summary__icontains=search)
            )

        category_id = self.request.GET.get('category', '')
        if category_id:
            query = query.filter(category_id=category_id)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': RouteCategory.objects.all(),
            'search': search,
            'category_id': category_id,
            'per_page': per_page,
        })
        return context


class HotelsListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/hotels_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Hotel.objects.all().order_by('-created_at')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(brief__icontains=search)
            )

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_obj': page_obj,
            'paginator': paginator,
            'search': search,
            'per_page': per_page,
        })
        return context


class NewsListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/news_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = News.objects.select_related('category', 'author').all().order_by('-published_at')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(content__icontains=search)
            )

        category_id = self.request.GET.get('category', '')
        if category_id:
            query = query.filter(category_id=category_id)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': NewsCategory.objects.all(),
            'search': search,
            'category_id': category_id,
            'per_page': per_page,
        })
        return context


class UsersListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/users_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = CustomUser.objects.all().order_by('-date_joined')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        account_type = self.request.GET.get('type', '')
        if account_type == 'staff':
            query = query.filter(is_staff=True)
        elif account_type == 'user':
            query = query.filter(is_staff=False)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'total': CustomUser.objects.count(),
            'paginator': paginator,
            'page_obj': page_obj,
            'search': search,
            'account_type': account_type,
            'per_page': per_page,
        })
        return context


class OrdersListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/orders_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = OrderDetail.objects.select_related('order', 'order__user').all().order_by('-id')

        # 搜索过滤
        item_name = self.request.GET.get('item_name', '')
        if item_name:
            query = query.filter(item_name__icontains=item_name)

        user_email = self.request.GET.get('user_email', '')
        if user_email:
            query = query.filter(order__user__email__icontains=user_email)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_obj': page_obj,
            'item_name': item_name,
            'user_email': user_email,
            'per_page': per_page,
        })
        return context


# ==================== 景点管理 CRUD ====================

class ScenicSpotCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = ScenicSpot
    form_class = ScenicSpotForm
    template_name = 'admin_panel/scenic_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '景点创建成功！')
        return reverse_lazy('admin_panel:scenic_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '新增景点'
        context['form_title'] = '新增景点'
        return context


class ScenicSpotUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = ScenicSpot
    form_class = ScenicSpotForm
    template_name = 'admin_panel/scenic_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '景点更新成功！')
        return reverse_lazy('admin_panel:scenic_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑景点'
        context['form_title'] = f'编辑景点：{self.object.name}'
        return context


class ScenicSpotDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = ScenicSpot
    template_name = 'admin_panel/scenic_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '景点删除成功！')
        return reverse_lazy('admin_panel:scenic_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除景点'
        return context


# ==================== 路线管理 CRUD ====================

class RouteCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'admin_panel/route_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '路线创建成功！')
        return reverse_lazy('admin_panel:routes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '新增路线'
        context['form_title'] = '新增路线'
        return context


class RouteUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'admin_panel/route_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '路线更新成功！')
        return reverse_lazy('admin_panel:routes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑路线'
        context['form_title'] = f'编辑路线：{self.object.name}'
        return context


class RouteDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Route
    template_name = 'admin_panel/route_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '路线删除成功！')
        return reverse_lazy('admin_panel:routes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除路线'
        return context


# ==================== 酒店管理 CRUD ====================

class HotelCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'admin_panel/hotel_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '酒店创建成功！')
        return reverse_lazy('admin_panel:hotels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '新增酒店'
        context['form_title'] = '新增酒店'
        return context


class HotelUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'admin_panel/hotel_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '酒店更新成功！')
        return reverse_lazy('admin_panel:hotels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑酒店'
        context['form_title'] = f'编辑酒店：{self.object.name}'
        return context


class HotelDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Hotel
    template_name = 'admin_panel/hotel_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '酒店删除成功！')
        return reverse_lazy('admin_panel:hotels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除酒店'
        return context


# ==================== 资讯管理 CRUD ====================

class NewsCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_panel/news_form.html'
    login_url = '/users/login/'

    def form_valid(self, form):
        # 如果没有选择作者，默认使用当前用户
        if not form.cleaned_data.get('author'):
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '资讯创建成功！')
        return reverse_lazy('admin_panel:news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '新增资讯'
        context['form_title'] = '新增资讯'
        return context


class NewsUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_panel/news_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '资讯更新成功！')
        return reverse_lazy('admin_panel:news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑资讯'
        context['form_title'] = f'编辑资讯：{self.object.title}'
        return context


class NewsDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = News
    template_name = 'admin_panel/news_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '资讯删除成功！')
        return reverse_lazy('admin_panel:news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除资讯'
        return context


# ==================== 用户管理 CRUD ====================

class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'admin_panel/user_form.html'
    login_url = '/users/login/'

    def form_valid(self, form):
        # 新建用户时必须设置密码
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if not password:
            form.add_error('password', '新建用户必须设置密码')
            return self.form_invalid(form)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '用户创建成功！')
        return reverse_lazy('admin_panel:users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '新增用户'
        context['form_title'] = '新增用户'
        return context


class UserUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'admin_panel/user_form.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '用户更新成功！')
        return reverse_lazy('admin_panel:users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑用户'
        context['form_title'] = f'编辑用户：{self.object.username}'
        return context


class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'admin_panel/user_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '用户删除成功！')
        return reverse_lazy('admin_panel:users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除用户'
        return context


# ==================== 订单管理 ====================

class OrderUpdateStatusView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = 'admin_panel/order_update_status.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '订单状态更新成功！')
        return reverse_lazy('admin_panel:orders_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '更新订单状态'
        context['form_title'] = f'更新订单状态：{self.object.order_sn}'
        return context


# ==================== 用户评价管理 ====================

class CommentsListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/comments_list.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Comment.objects.select_related('user').all().order_by('-created_at')

        # 搜索过滤
        search = self.request.GET.get('search', '')
        if search:
            query = query.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(content__icontains=search)
            )

        target_type = self.request.GET.get('target_type', '')
        if target_type:
            query = query.filter(target_type=target_type)

        is_deleted = self.request.GET.get('is_deleted', '')
        if is_deleted == 'true':
            query = query.filter(is_deleted=True)
        elif is_deleted == 'false':
            query = query.filter(is_deleted=False)

        # 分页
        try:
            per_page = int(self.request.GET.get('per_page', 10))
            if per_page not in [10, 20, 50]:
                per_page = 10
        except (ValueError, TypeError):
            per_page = 10
        paginator = Paginator(query, per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_obj': page_obj,
            'search': search,
            'target_type': target_type,
            'is_deleted': is_deleted,
            'per_page': per_page,
            'target_type_choices': Comment.CONTENT_TYPE_CHOICES,
        })
        return context


class CommentDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Comment
    template_name = 'admin_panel/comment_confirm_delete.html'
    login_url = '/users/login/'

    def get_success_url(self):
        messages.success(self.request, '评价删除成功！')
        return reverse_lazy('admin_panel:comments_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除评价'
        return context
