from django.http import JsonResponse
from django.views import View

# API 视图骨架
class CategoryListView(View):
    def get(self, request):
        # 获取景点分类列表
        categories = [{"id": 1, "name": "自然景观"}, {"id": 2, "name": "人文古迹"}]
        return JsonResponse({"status": "success", "data": categories})

class SpotListView(View):
    def get(self, request):
        # 获取景点列表，支持筛选、排git init序、分页
        # request.GET.get('category')
        # request.GET.get('sort')
        # request.GET.get('page')
        spots = [{"id": 1, "name": "白洋淀", "price": "100.00", "rating": 4.8, "image": "/media/placeholder.jpg"}]
        return JsonResponse({"status": "success", "data": spots, "total": 1})

class SpotDetailView(View):
    def get(self, request, pk):
        # 获取景点详情
        spot_detail = {
            "id": pk,
            "name": "白洋淀",
            "price": "100.00",
            "address": "保定市安新县",
            "open_time": "08:00-18:00",
            "description": "白洋淀是...",
            "images": [{"url": "/media/placeholder.jpg"}],
            "reviews": []
        }
        return JsonResponse({"status": "success", "data": spot_detail})