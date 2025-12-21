from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AIAssistantView(TemplateView):
    """
    AI助手页面视图
    """
    template_name = 'ai_assistant/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'AI旅游助手'
        return context


class AIHistoryView(LoginRequiredMixin, TemplateView):
    """
    AI查询历史页面
    """
    template_name = 'ai_assistant/history.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '我的AI规划历史'
        return context

