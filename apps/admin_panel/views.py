from django.views.generic import TemplateView
from django.db.models import Count
from apps.scenic.models import ScenicSpot
from apps.routes.models import Route
from apps.users.models import CustomUser
from apps.orders.models import Order


# (你需要添加 @method_decorator(staff_member_required) 来保护这个页面)

class AdminIndexView(TemplateView):
    template_name = "admin_panel/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '后台管理'

        # 热门景点排行 (按收藏数)
        context['hot_spots'] = ScenicSpot.objects.annotate(
            num_favorites=Count('favorite')  # 'favorite' 来自 Favorite 模型的 related_name (如果设置了)
        ).order_by('-num_favorites')[:5]  # 假设 Favorite 中 target_type='scenic'

        # 热门路线排行 (按订单数)
        context['hot_routes'] = Route.objects.annotate(
            num_orders=Count('orderdetail')  # 假设 OrderDetail 中 target_type='route'
        ).order_by('-num_orders')[:5]

        # 数据统计
        context['total_users'] = CustomUser.objects.count()
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='pending').count()

        return context