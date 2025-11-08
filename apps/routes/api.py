from django.http import JsonResponse
from django.views import View

class RouteCategoryListView(View):
    def get(self, request):
        categories = [{"id": 1, "name": "历史文化"}, {"id": 2, "name": "自然风光"}]
        return JsonResponse({"status": "success", "data": categories})

class RouteListView(View):
    def get(self, request):
        routes = [{"id": 1, "name": "保定2日游", "price": "500.00", "days": 2, "image": "/media/placeholder.jpg"}]
        return JsonResponse({"status": "success", "data": routes, "total": 1})

class RouteDetailView(View):
    def get(self, request, pk):
        route_detail = {
            "id": pk,
            "name": "保定2日游",
            "price": "500.00",
            "itineraries": [
                {"day": 1, "title": "古莲花池 -> 直隶总督署", "description": "..."},
                {"day": 2, "title": "白洋淀一日游", "description": "..."}
            ],
            "cost_include": "...",
            "notes": "..."
        }
        return JsonResponse({"status": "success", "data": route_detail})