from django.http import JsonResponse
from django.views import View

class NewsCategoryListView(View):
    def get(self, request):
        categories = [{"id": 1, "name": "旅游攻略"}, {"id": 2, "name": "新闻动态"}]
        return JsonResponse({"status": "success", "data": categories})

class NewsListView(View):
    def get(self, request):
        news = [{"id": 1, "title": "保定旅游全攻略", "abstract": "...", "published_at": "2025-11-04"}]
        return JsonResponse({"status": "success", "data": news, "total": 1})

class NewsDetailView(View):
    def get(self, request, pk):
        news_detail = {"id": pk, "title": "保定旅游全攻略", "content": "...", "views": 100, "comments": []}
        return JsonResponse({"status": "success", "data": news_detail})

class CommentAPIView(View):
    def post(self, request, pk):
        # 提交对 pk 资讯的评论
        return JsonResponse({"status": "success", "message": "评论成功"})