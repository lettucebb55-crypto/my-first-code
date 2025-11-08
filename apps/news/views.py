from django.views.generic import TemplateView

class NewsListView(TemplateView):
    template_name = "news/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '资讯列表'
        return context

class NewsDetailView(TemplateView):
    template_name = "news/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk = kwargs.get('pk')
        context['page_title'] = "资讯详情"
        return context