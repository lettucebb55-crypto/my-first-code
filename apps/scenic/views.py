from django.views.generic import TemplateView

class ScenicListView(TemplateView):
    # 修正：指向景点列表模板
    template_name = "scenic/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '景点列表'
        # 此处填充景点列表、分类、筛选条件等数据
        return context

class ScenicDetailView(TemplateView):
    # 修正：这个路径也需要清理
    template_name = "scenic/detail.html" # 原本是 "scenic/../../templates/routes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk = kwargs.get('pk')
        # spot = ScenicSpot.objects.get(pk=pk)
        context['page_title'] = "景点详情" # f"{spot.name} - 景点详情"
        # context['spot'] = spot
        return context