from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from .models import Food, FoodCategory


class FoodListAPIView(View):
    """
    美食列表API
    GET /api/v1/foods/
    参数：
    - category: 分类ID
    - search: 搜索关键词
    - is_hot: 是否热门（1/0）
    - is_traditional: 是否传统美食（1/0）
    - page: 页码
    - page_size: 每页数量
    """
    
    def get(self, request):
        try:
            queryset = Food.objects.select_related('category').prefetch_related('images').all()
            
            # 分类筛选
            category_id = request.GET.get('category')
            if category_id:
                queryset = queryset.filter(category_id=category_id)
            
            # 搜索
            search = request.GET.get('search')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(ingredients__icontains=search) |
                    Q(tags__icontains=search)
                )
            
            # 筛选条件
            if request.GET.get('is_hot') == '1':
                queryset = queryset.filter(is_hot=True)
            
            if request.GET.get('is_traditional') == '1':
                queryset = queryset.filter(is_traditional=True)
            
            # 排序
            queryset = queryset.order_by('-is_hot', '-is_recommended', '-rating', '-created_at')
            
            # 分页
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            total = queryset.count()
            start = (page - 1) * page_size
            end = start + page_size
            foods = queryset[start:end]
            
            # 构建返回数据
            food_list = []
            for food in foods:
                images = food.images.all()
                food_list.append({
                    "id": food.id,
                    "name": food.name,
                    "english_name": food.english_name,
                    "category": {
                        "id": food.category.id if food.category else None,
                        "name": food.category.name if food.category else None,
                    },
                    "description": food.description[:200] + '...' if len(food.description) > 200 else food.description,
                    "cover_image": food.cover_image.url if food.cover_image else None,
                    "price_range": food.price_range,
                    "average_price": float(food.average_price) if food.average_price else None,
                    "is_hot": food.is_hot,
                    "is_recommended": food.is_recommended,
                    "is_traditional": food.is_traditional,
                    "rating": float(food.rating),
                    "views_count": food.views_count,
                    "tags": food.get_tags_list(),
                })
            
            return JsonResponse({
                "status": "success",
                "data": food_list,
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
                "message": f"获取美食列表失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class FoodDetailAPIView(View):
    """
    美食详情API
    GET /api/v1/foods/<id>/
    """
    
    def get(self, request, food_id):
        try:
            food = Food.objects.select_related('category').prefetch_related('images').get(id=food_id)
            
            # 增加浏览次数
            food.views_count += 1
            food.save(update_fields=['views_count'])
            
            # 获取图片
            images = food.images.all()
            image_list = [{
                "url": img.image.url,
                "description": img.description
            } for img in images]
            
            data = {
                "id": food.id,
                "name": food.name,
                "english_name": food.english_name,
                "category": {
                    "id": food.category.id if food.category else None,
                    "name": food.category.name if food.category else None,
                },
                "description": food.description,
                "ingredients": food.ingredients,
                "cooking_method": food.cooking_method,
                "cultural_background": food.cultural_background,
                "cover_image": food.cover_image.url if food.cover_image else None,
                "images": image_list,
                "price_range": food.price_range,
                "average_price": float(food.average_price) if food.average_price else None,
                "is_hot": food.is_hot,
                "is_recommended": food.is_recommended,
                "is_traditional": food.is_traditional,
                "rating": float(food.rating),
                "views_count": food.views_count,
                "tags": food.get_tags_list(),
                "recommended_restaurants": food.get_restaurants_list(),
                "created_at": food.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            return JsonResponse({
                "status": "success",
                "data": data
            })
            
        except Food.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "美食不存在"
            }, status=404)
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "error",
                "message": f"获取美食详情失败：{str(e)}",
                "debug": traceback.format_exc() if request.user.is_staff else None
            }, status=500)


class FoodCategoryListAPIView(View):
    """
    美食分类列表API
    GET /api/v1/foods/categories/
    """
    
    def get(self, request):
        try:
            categories = FoodCategory.objects.all()
            category_list = [{
                "id": cat.id,
                "name": cat.name,
                "description": cat.description,
                "icon": cat.icon,
            } for cat in categories]
            
            return JsonResponse({
                "status": "success",
                "data": category_list
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"获取分类列表失败：{str(e)}"
            }, status=500)

