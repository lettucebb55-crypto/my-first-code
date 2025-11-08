from django.views.generic import TemplateView

class ScenicListView(TemplateView):
    template_name = "scenic/../../templates/routes/../../templates/scenic/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '景点列表'
        # 此处填充景点列表、分类、筛选条件等数据
        return context

class ScenicDetailView(TemplateView):
    template_name = "scenic/../../templates/routes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk = kwargs.get('pk')
        # spot = ScenicSpot.objects.get(pk=pk)
        context['page_title'] = "景点详情" # f"{spot.name} - 景点详情"
        # context['spot'] = spot
        return context