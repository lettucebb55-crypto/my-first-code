from django.http import JsonResponse
from django.views import View
from .models import Order  # 确保导入 Order 模型


# 1. 恢复：原有的创建订单视图
class OrderCreateAPIView(View):
    def post(self, request):
        # 创建订单逻辑
        # 1. 获取前端提交的 (item_id, item_type, quantity, contact_info)
        # 2. 验证库存/价格 (如果需要)
        # 3. 创建 Order 和 OrderDetail
        # 4. 返回订单号和支付信息
        order_sn = "BD202511040001"
        return JsonResponse({"status": "success", "message": "订单创建成功", "order_sn": order_sn})


# 2. 恢复：原有的订单列表视图
class OrderListAPIView(View):
    def get(self, request):
        # 获取当前用户的订单列表 (需要登录)
        # request.GET.get('status') # 按状态筛选
        orders = [{"order_sn": "BD202511040001", "status": "待支付", "total": 500.00}]
        return JsonResponse({"status": "success", "data": orders})


# 3. 恢复：原有的订单详情视图
class OrderDetailAPIView(View):
    def get(self, request, order_sn):
        # 获取订单详情 (需要登录和权限验证)
        order_detail = {
            "order_sn": order_sn,
            "status": "待支付",
            "total": 500.00,
            "contact_name": "张三",
            "details": [
                {"item_name": "保定2日游", "price": 500.00, "quantity": 1}
            ]
        }
        return JsonResponse({"status": "success", "data": order_detail})


# 4. 保留：我们新增的取消订单视图
class OrderCancelAPIView(View):
    """
    处理取消订单 (使用 PUT/PATCH 方法更新状态)
    """

    def put(self, request, order_sn):
        # 1. 检查用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "请先登录"}, status=401)

        try:
            # 2. 获取订单，并确保订单是属于当前用户的
            order = Order.objects.get(order_sn=order_sn, user=request.user)

            # 3. 只有 'pending' (待支付) 状态的订单才能被取消
            if order.status == 'pending':
                order.status = 'cancelled'  # 更新状态
                order.save()
                return JsonResponse({"status": "success", "message": "订单已取消"})
            else:
                return JsonResponse({"status": "error", "message": "当前状态无法取消订单"}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "订单未找到"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)