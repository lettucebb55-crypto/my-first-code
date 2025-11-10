from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# 导入你的表单和模型
# (如果还没创建 forms.py，请先创建)
from .forms import CustomUserCreationForm
from .models import CustomUser

# --- 1. 你原来就有的视图 (来自你的文件) ---
class UserHomeView(TemplateView):
    template_name = "user/home.html"
    # 需要用户登录 (后续添加LoginRequiredMixin)

class UserProfileView(TemplateView):
    template_name = "user/profile.html"
    # 需要用户登录

class UserOrdersView(TemplateView):
    template_name = "user/orders.html"
    # 需要用户登录

class UserFavoritesView(TemplateView):
    template_name = "user/favorites.html"
    # 需要用户登录

class UserReviewsView(TemplateView):
    template_name = "user/reviews.html"
    # 需要用户登录

# --- 2. 上一步建议添加的视图 (用于登录/注册) ---
class LoginView(auth_views.LoginView):
    """
    使用 Django 内置的 LoginView
    """
    template_name = 'users/login.html'
    next_page = reverse_lazy('users:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '登录'
        return context

class RegisterView(CreateView):
    """
    使用 Django 内置的 CreateView
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '注册'
        return context