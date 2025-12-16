from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Comment


@method_decorator(csrf_exempt, name='dispatch')
class CommentAPIView(LoginRequiredMixin, View):
    """评论功能API - 用户删除自己的评论"""
    
    def delete(self, request, comment_id=None):
        """删除评论（软删除）"""
        try:
            # 从URL路径参数获取评论ID（优先）
            if comment_id:
                comment_id = int(comment_id)
            else:
                # 从请求体或查询参数获取评论ID
                if request.content_type == 'application/json' and request.body:
                    try:
                        data = json.loads(request.body)
                        comment_id = data.get('comment_id')
                    except:
                        pass
                
                if not comment_id:
                    comment_id = request.POST.get('comment_id') or request.GET.get('comment_id')
            
            if not comment_id:
                return JsonResponse({
                    "status": "error",
                    "message": "缺少必要参数：comment_id"
                }, status=400)
            
            # 获取评论对象
            try:
                comment = Comment.objects.get(pk=int(comment_id))
            except Comment.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "评论不存在"
                }, status=404)
            
            # 检查是否是评论所有者
            if comment.user != request.user:
                return JsonResponse({
                    "status": "error",
                    "message": "无权删除此评论"
                }, status=403)
            
            # 软删除：标记为已删除
            comment.is_deleted = True
            comment.save()
            
            return JsonResponse({
                "status": "success",
                "message": "评论删除成功"
            })
            
        except ValueError:
            return JsonResponse({
                "status": "error",
                "message": "无效的评论ID"
            }, status=400)
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"删除失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)

