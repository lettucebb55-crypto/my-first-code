from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
import json
from .models import CheckIn, CheckInPhoto
from apps.scenic.models import ScenicSpot


class CheckInCreateAPIView(LoginRequiredMixin, View):
    """
    创建打卡记录API
    POST /api/v1/checkins/
    参数：
    - scenic_spot_id: 景点ID（必填）
    - checkin_time: 打卡时间（可选，默认当前时间）
    - latitude: 打卡纬度（可选）
    - longitude: 打卡经度（可选）
    - notes: 备注（可选）
    - is_public: 是否公开（可选，默认True）
    - photos: 照片文件列表（可选，通过FormData上传）
    """
    
    def post(self, request):
        try:
            # 获取景点ID
            scenic_spot_id = request.POST.get('scenic_spot_id') or (
                json.loads(request.body).get('scenic_spot_id') if request.content_type == 'application/json' else None
            )
            
            if not scenic_spot_id:
                return JsonResponse({
                    "status": "error",
                    "message": "缺少必要参数：scenic_spot_id"
                }, status=400)
            
            # 验证景点是否存在
            try:
                scenic_spot = ScenicSpot.objects.get(id=int(scenic_spot_id))
            except ScenicSpot.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "景点不存在"
                }, status=404)
            
            # 获取打卡时间
            checkin_time_str = request.POST.get('checkin_time')
            if checkin_time_str:
                from django.utils.dateparse import parse_datetime
                checkin_time = parse_datetime(checkin_time_str)
                if not checkin_time:
                    checkin_time = timezone.now()
            else:
                checkin_time = timezone.now()
            
            # 获取其他参数
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            notes = request.POST.get('notes', '')
            is_public = request.POST.get('is_public', 'true').lower() == 'true'
            
            # 创建打卡记录
            checkin = CheckIn.objects.create(
                user=request.user,
                scenic_spot=scenic_spot,
                checkin_time=checkin_time,
                latitude=float(latitude) if latitude else None,
                longitude=float(longitude) if longitude else None,
                notes=notes,
                is_public=is_public
            )
            
            # 处理主照片（第一张上传的照片作为主照片）
            main_photo = request.FILES.get('main_photo') or request.FILES.get('photo')
            if main_photo:
                checkin.main_photo = main_photo
                checkin.save()
            
            # 处理多张照片
            photos = request.FILES.getlist('photos')
            if not photos and main_photo:
                photos = [main_photo]
            
            for index, photo_file in enumerate(photos):
                CheckInPhoto.objects.create(
                    checkin=checkin,
                    photo=photo_file,
                    order=index
                )
            
            # 返回创建结果
            return JsonResponse({
                "status": "success",
                "message": "打卡成功",
                "data": {
                    "id": checkin.id,
                    "scenic_spot_id": checkin.scenic_spot.id,
                    "scenic_spot_name": checkin.scenic_spot.name,
                    "checkin_time": checkin.checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "main_photo": checkin.main_photo.url if checkin.main_photo else None,
                    "notes": checkin.notes,
                    "is_public": checkin.is_public
                }
            })
            
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"打卡失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class CheckInListAPIView(LoginRequiredMixin, View):
    """
    获取打卡记录列表API
    GET /api/v1/checkins/
    参数：
    - user_id: 用户ID（可选，默认当前用户，管理员可查看其他用户）
    - scenic_spot_id: 景点ID（可选，筛选特定景点）
    - page: 页码（可选，默认1）
    - page_size: 每页数量（可选，默认10）
    """
    
    def get(self, request):
        try:
            # 获取参数
            user_id = request.GET.get('user_id')
            scenic_spot_id = request.GET.get('scenic_spot_id')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            
            # 构建查询
            queryset = CheckIn.objects.all()
            
            # 权限控制：普通用户只能查看自己的，管理员可以查看所有
            if not request.user.is_staff:
                queryset = queryset.filter(user=request.user)
            elif user_id:
                queryset = queryset.filter(user_id=user_id)
            
            # 筛选景点
            if scenic_spot_id:
                queryset = queryset.filter(scenic_spot_id=scenic_spot_id)
            
            # 排序
            queryset = queryset.order_by('-checkin_time')
            
            # 分页
            total = queryset.count()
            start = (page - 1) * page_size
            end = start + page_size
            checkins = queryset[start:end]
            
            # 构建返回数据
            checkin_list = []
            for checkin in checkins:
                # 获取所有照片
                photos = checkin.photos.all()
                photo_urls = [photo.photo.url for photo in photos]
                
                checkin_list.append({
                    "id": checkin.id,
                    "scenic_spot": {
                        "id": checkin.scenic_spot.id,
                        "name": checkin.scenic_spot.name,
                        "address": checkin.scenic_spot.address,
                        "cover_image": checkin.scenic_spot.cover_image.url if checkin.scenic_spot.cover_image else None,
                        "latitude": float(checkin.scenic_spot.latitude) if checkin.scenic_spot.latitude else None,
                        "longitude": float(checkin.scenic_spot.longitude) if checkin.scenic_spot.longitude else None,
                    },
                    "checkin_time": checkin.checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "main_photo": checkin.main_photo.url if checkin.main_photo else None,
                    "photos": photo_urls,
                    "latitude": float(checkin.latitude) if checkin.latitude else None,
                    "longitude": float(checkin.longitude) if checkin.longitude else None,
                    "notes": checkin.notes,
                    "is_public": checkin.is_public,
                    "created_at": checkin.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return JsonResponse({
                "status": "success",
                "data": checkin_list,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": (total + page_size - 1) // page_size
                }
            })
            
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"获取打卡列表失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class CheckInMapAPIView(LoginRequiredMixin, View):
    """
    获取个人旅游地图数据API
    GET /api/v1/checkins/map/
    返回用户所有打卡记录的经纬度信息，用于在地图上展示
    """
    
    def get(self, request):
        try:
            # 获取当前用户的所有公开打卡记录
            checkins = CheckIn.objects.filter(
                user=request.user,
                is_public=True
            ).select_related('scenic_spot').order_by('-checkin_time')
            
            # 构建地图数据
            map_data = []
            for checkin in checkins:
                # 优先使用打卡时的位置，如果没有则使用景点位置
                lat = float(checkin.latitude) if checkin.latitude else (
                    float(checkin.scenic_spot.latitude) if checkin.scenic_spot.latitude else None
                )
                lng = float(checkin.longitude) if checkin.longitude else (
                    float(checkin.scenic_spot.longitude) if checkin.scenic_spot.longitude else None
                )
                
                if lat and lng:
                    map_data.append({
                        "id": checkin.id,
                        "scenic_spot": {
                            "id": checkin.scenic_spot.id,
                            "name": checkin.scenic_spot.name,
                            "address": checkin.scenic_spot.address,
                            "cover_image": checkin.scenic_spot.cover_image.url if checkin.scenic_spot.cover_image else None,
                        },
                        "latitude": lat,
                        "longitude": lng,
                        "checkin_time": checkin.checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "main_photo": checkin.main_photo.url if checkin.main_photo else None,
                        "notes": checkin.notes
                    })
            
            # 统计信息
            stats = {
                "total_checkins": checkins.count(),
                "total_spots": checkins.values('scenic_spot').distinct().count(),
                "first_checkin": checkins.last().checkin_time.strftime('%Y-%m-%d') if checkins.exists() else None,
                "last_checkin": checkins.first().checkin_time.strftime('%Y-%m-%d') if checkins.exists() else None,
            }
            
            return JsonResponse({
                "status": "success",
                "data": map_data,
                "stats": stats
            })
            
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"获取地图数据失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class CheckInDetailAPIView(LoginRequiredMixin, View):
    """
    获取打卡记录详情API
    GET /api/v1/checkins/<id>/
    """
    
    def get(self, request, checkin_id):
        try:
            checkin = CheckIn.objects.select_related('scenic_spot', 'user').prefetch_related('photos').get(id=checkin_id)
            
            # 权限检查：只能查看自己的打卡记录，除非是管理员
            if not request.user.is_staff and checkin.user != request.user:
                return JsonResponse({
                    "status": "error",
                    "message": "无权访问此打卡记录"
                }, status=403)
            
            # 获取所有照片
            photos = checkin.photos.all()
            photo_urls = [photo.photo.url for photo in photos]
            
            data = {
                "id": checkin.id,
                "user": {
                    "id": checkin.user.id,
                    "username": checkin.user.username,
                    "avatar": checkin.user.avatar.url if checkin.user.avatar else None
                },
                "scenic_spot": {
                    "id": checkin.scenic_spot.id,
                    "name": checkin.scenic_spot.name,
                    "address": checkin.scenic_spot.address,
                    "cover_image": checkin.scenic_spot.cover_image.url if checkin.scenic_spot.cover_image else None,
                    "latitude": float(checkin.scenic_spot.latitude) if checkin.scenic_spot.latitude else None,
                    "longitude": float(checkin.scenic_spot.longitude) if checkin.scenic_spot.longitude else None,
                },
                "checkin_time": checkin.checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
                "main_photo": checkin.main_photo.url if checkin.main_photo else None,
                "photos": photo_urls,
                "latitude": float(checkin.latitude) if checkin.latitude else None,
                "longitude": float(checkin.longitude) if checkin.longitude else None,
                "notes": checkin.notes,
                "is_public": checkin.is_public,
                "created_at": checkin.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": checkin.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return JsonResponse({
                "status": "success",
                "data": data
            })
            
        except CheckIn.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "打卡记录不存在"
            }, status=404)
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"获取打卡详情失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class CheckInDeleteAPIView(LoginRequiredMixin, View):
    """
    删除打卡记录API
    DELETE /api/v1/checkins/<id>/
    """
    
    def delete(self, request, checkin_id):
        try:
            checkin = CheckIn.objects.get(id=checkin_id)
            
            # 权限检查：只能删除自己的打卡记录，除非是管理员
            if not request.user.is_staff and checkin.user != request.user:
                return JsonResponse({
                    "status": "error",
                    "message": "无权删除此打卡记录"
                }, status=403)
            
            checkin.delete()
            
            return JsonResponse({
                "status": "success",
                "message": "删除成功"
            })
            
        except CheckIn.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "打卡记录不存在"
            }, status=404)
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"删除失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)

