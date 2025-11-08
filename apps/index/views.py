from django.views.generic import TemplateView

# 首页视图
class IndexView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '首页 - 保定旅游网'
        # 此处填充首页所需数据，如轮播图、热门景点等
        # context['carousels'] = ...
        # context['hot_spots'] = ...
        return context