from django.views.generic import TemplateView

class RouteListView(TemplateView):
    # 修正：指向路线列表模板
    template_name = "routes/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '路线列表'
        return context

class RouteDetailView(TemplateView):
    template_name = "routes/detail.html"

    # 正确的代码
    def get_context_data(self, **kwargs):
        # 1. 必须先从父类获取 context
        context = super().get_context_data(**kwargs)

        # 2. 然后才能修改或添加内容
        # pk = kwargs.get('pk')
        context['page_title'] = "路线详情"

        # 3. 最后返回修改后的 context
        return context