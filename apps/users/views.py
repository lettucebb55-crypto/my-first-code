from django.views.generic import TemplateView
from django.http import HttpResponse

# 简单的视图骨架，后续填充逻辑
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