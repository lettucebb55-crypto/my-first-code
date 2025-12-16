from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from .models import Favorite


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


class FavoriteAPIView(LoginRequiredMixin, View):
    """收藏功能API"""
    
    def get(self, request):
        """获取收藏列表"""
        try:
            target_type = request.GET.get('target_type', 'scenic')
            favorites = Favorite.objects.filter(
                user=request.user,
                target_type=target_type
            ).order_by('-created_at')
            
            favorite_list = []
            for fav in favorites:
                favorite_list.append({
                    'id': fav.id,
                    'target_id': fav.target_id,
                    'target_type': fav.target_type,
                    'created_at': fav.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return JsonResponse({
                "status": "success",
                "data": favorite_list
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    def post(self, request):
        """添加收藏"""
        try:
            # 获取参数
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                target_id = data.get('target_id')
                target_type = data.get('target_type', 'scenic')
            else:
                target_id = request.POST.get('target_id')
                target_type = request.POST.get('target_type', 'scenic')
            
            if not target_id:
                return JsonResponse({
                    "status": "error",
                    "message": "缺少必要参数"
                }, status=400)
            
            # 检查是否已收藏
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                target_id=int(target_id),
                target_type=target_type
            )
            
            if created:
                return JsonResponse({
                    "status": "success",
                    "message": "收藏成功",
                    "is_favorited": True
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "已经收藏过了",
                    "is_favorited": True
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"收藏失败：{str(e)}"
            }, status=500)

    def delete(self, request):
        """取消收藏"""
        try:
            # DELETE请求通常从URL参数或查询参数获取数据
            # 也可以从request.body获取JSON数据
            target_id = None
            target_type = 'scenic'
            
            # 先尝试从URL查询参数获取
            target_id = request.GET.get('target_id')
            target_type = request.GET.get('target_type', 'scenic')
            
            # 如果查询参数没有，尝试从body获取JSON
            if not target_id and request.body:
                try:
                    data = json.loads(request.body)
                    target_id = data.get('target_id')
                    target_type = data.get('target_type', 'scenic')
                except:
                    pass
            
            # 如果还是没有，尝试从POST获取（某些情况下）
            if not target_id:
                target_id = request.POST.get('target_id')
                target_type = request.POST.get('target_type', 'scenic')
            
            if not target_id:
                return JsonResponse({
                    "status": "error",
                    "message": "缺少必要参数：target_id"
                }, status=400)
            
            # 删除收藏
            deleted = Favorite.objects.filter(
                user=request.user,
                target_id=int(target_id),
                target_type=target_type
            ).delete()
            
            if deleted[0] > 0:
                return JsonResponse({
                    "status": "success",
                    "message": "取消收藏成功",
                    "is_favorited": False
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "未找到收藏记录",
                    "is_favorited": False
                }, status=404)
                
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"取消收藏失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)
    
    def get_favorite_status(self, request, target_id, target_type='scenic'):
        """检查是否已收藏（辅助方法）"""
        is_favorited = Favorite.objects.filter(
            user=request.user,
            target_id=target_id,
            target_type=target_type
        ).exists()
        return is_favorited