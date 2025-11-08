from django.http import JsonResponse
from django.views import View

class OrderCreateAPIView(View):
    def post(self, request):
        # 创建订单逻辑
        # 1. 获取前端提交的 (item_id, item_type, quantity, contact_info)
        # 2. 验证库存/价格 (如果需要)
        # 3. 创建 Order 和 OrderDetail
        # 4. 返回订单号和支付信息
        order_sn = "BD202511040001"
        return JsonResponse({"status": "success", "message": "订单创建成功", "order_sn": order_sn})

class OrderListAPIView(View):
    def get(self, request):
        # 获取当前用户的订单列表 (需要登录)
        # request.GET.get('status') # 按状态筛选
        orders = [{"order_sn": "BD202511040001", "status": "待支付", "total": 500.00}]
        return JsonResponse({"status": "success", "data": orders})

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