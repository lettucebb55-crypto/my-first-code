from django.views.generic import TemplateView


class AdminIndexView(TemplateView):
    template_name = "admin_panel/index.html"

    # 此处应添加权限验证 (例如 @method_decorator(staff_member_required))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '后台管理'
        # 填充后台首页所需的数据
        # context['total_users'] = ...
        # context['total_orders'] = ...
        return context

# 此处可以添加景点管理、路线管理、资讯管理等的增删改查视图
# (例如使用 ModelForm 或 DRF 的 ViewSet)