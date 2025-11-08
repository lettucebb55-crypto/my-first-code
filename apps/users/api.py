from django.http import JsonResponse
from django.views import View


# API 视图骨架
class RegisterAPIView(View):
    def post(self, request):
        # 处理注册逻辑
        return JsonResponse({"status": "success", "message": "注册成功"})


class LoginAPIView(View):
    def post(self, request):
        # 处理登录逻辑
        return JsonResponse({"status": "success", "message": "登录成功", "token": "YOUR_JWT_TOKEN_HERE"})


class ProfileAPIView(View):
    def get(self, request):
        # 获取用户信息
        return JsonResponse({"status": "success", "data": {"username": "test", "phone": "13800138000"}})

    def put(self, request):
        # 更新用户信息
        return JsonResponse({"status": "success", "message": "更新成功"})


class FavoriteAPIView(View):
    def get(self, request):
        # 获取收藏列表
        return JsonResponse({"status": "success", "data": []})

    def post(self, request):
        # 添加收藏
        return JsonResponse({"status": "success", "message": "收藏成功"})

    def delete(self, request):
        # 取消收藏
        return JsonResponse({"status": "success", "message": "取消收藏成功"})