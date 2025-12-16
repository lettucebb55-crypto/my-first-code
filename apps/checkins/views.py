from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from apps.scenic.models import ScenicSpot


class CheckInListView(LoginRequiredMixin, TemplateView):
    """
    打卡记录列表页面
    """
    template_name = 'checkins/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CheckInMapView(LoginRequiredMixin, TemplateView):
    """
    个人旅游地图页面
    """
    template_name = 'checkins/map.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CheckInCreateView(LoginRequiredMixin, TemplateView):
    """
    打卡页面
    """
    template_name = 'checkins/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenic_spot_id = kwargs.get('scenic_spot_id')
        context['scenic_spot'] = get_object_or_404(ScenicSpot, id=scenic_spot_id)
        context['user'] = self.request.user
        return context
