from django.views.generic import TemplateView

class RouteListView(TemplateView):
    template_name = "routes/../../templates/scenic/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '路线列表'
        return context

class RouteDetailView(TemplateView):
    template_name = "routes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk = kwargs.get('pk')
        context['page_title'] = "路线详情"
        return context