from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Order, OrderDetail
from apps.scenic.models import ScenicSpot
from apps.routes.models import Route
from apps.hotels.models import Hotel, RoomType


class OrderConfirmView(LoginRequiredMixin, TemplateView):
    template_name = "orders/confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '订单确认'
        
        # 获取订单参数
        item_id = self.request.GET.get('item_id')
        item_type = self.request.GET.get('item_type')
        quantity = int(self.request.GET.get('quantity', 1))
        contact_name = self.request.GET.get('contact_name', '')
        contact_phone = self.request.GET.get('contact_phone', '')
        booking_date = self.request.GET.get('booking_date', '')
        
        context['item_id'] = item_id
        context['item_type'] = item_type
        context['quantity'] = quantity
        context['contact_name'] = contact_name
        context['contact_phone'] = contact_phone
        context['booking_date'] = booking_date
        
        # 获取项目信息
        item = None
        price = 0
        if item_type == 'scenic' and item_id:
            try:
                item = ScenicSpot.objects.get(pk=item_id)
                price = item.ticket_price
            except ScenicSpot.DoesNotExist:
                pass
        elif item_type == 'route' and item_id:
            try:
                item = Route.objects.get(pk=item_id)
                price = item.price
            except Route.DoesNotExist:
                pass
        elif item_type == 'hotel' and item_id:
            try:
                item = Hotel.objects.get(pk=item_id)
                # 酒店价格取最低房间价格
                room_type = RoomType.objects.filter(hotel=item, is_available=True).order_by('price').first()
                if room_type:
                    price = room_type.price
            except Hotel.DoesNotExist:
                pass
        
        context['item'] = item
        context['price'] = price
        context['total'] = price * quantity
        
        return context


class OrderPaymentView(LoginRequiredMixin, View):
    """订单支付视图 - 创建订单并处理支付"""
    
    def get(self, request, order_sn=None):
        # 如果是模拟支付成功
        if request.GET.get('success') == '1':
            return self.handle_payment_success(request, order_sn)
        
        # 显示支付页面
        from django.views.generic import TemplateView
        from django.template.response import TemplateResponse
        
        context = {
            'page_title': '订单支付',
            'order_sn': order_sn,
        }
        
        # 获取订单信息
        try:
            order = Order.objects.get(order_sn=order_sn, user=request.user)
            context['order'] = order
        except Order.DoesNotExist:
            pass
        
        return TemplateResponse(request, "orders/payment.html", context)
    
    def post(self, request, order_sn=None):
        """处理支付请求"""
        # 获取订单参数
        item_id = request.POST.get('item_id')
        item_type = request.POST.get('item_type')
        quantity = int(request.POST.get('quantity', 1))
        contact_name = request.POST.get('contact_name', '')
        contact_phone = request.POST.get('contact_phone', '')
        
        if not all([item_id, item_type, contact_name, contact_phone]):
            return JsonResponse({'status': 'error', 'message': '参数不完整'})
        
        # 创建订单
        order = self.create_order(request.user, item_id, item_type, quantity, contact_name, contact_phone)
        
        if order:
            return HttpResponseRedirect(f'/orders/payment/{order.order_sn}/')
        else:
            return JsonResponse({'status': 'error', 'message': '订单创建失败'})
    
    def create_order(self, user, item_id, item_type, quantity, contact_name, contact_phone):
        """创建订单"""
        try:
            # 生成订单号
            order_sn = f"BD{timezone.now().strftime('%Y%m%d')}{get_random_string(6, '0123456789')}"
            
            # 获取项目信息和价格
            item_name = ''
            price = 0
            
            if item_type == 'scenic':
                item = ScenicSpot.objects.get(pk=item_id)
                item_name = item.name
                price = item.ticket_price
            elif item_type == 'route':
                item = Route.objects.get(pk=item_id)
                item_name = item.name
                price = item.price
            elif item_type == 'hotel':
                item = Hotel.objects.get(pk=item_id)
                item_name = item.name
                room_type = RoomType.objects.filter(hotel=item, is_available=True).order_by('price').first()
                if room_type:
                    price = room_type.price
                else:
                    return None
            else:
                return None
            
            total_amount = price * quantity
            
            # 创建订单
            order = Order.objects.create(
                order_sn=order_sn,
                user=user,
                total_amount=total_amount,
                status='pending',
                contact_name=contact_name,
                contact_phone=contact_phone
            )
            
            # 创建订单明细
            OrderDetail.objects.create(
                order=order,
                item_type=item_type,
                item_id=item_id,
                item_name=item_name,
                price=price,
                quantity=quantity,
                subtotal=total_amount
            )
            
            return order
        except Exception as e:
            print(f"创建订单失败: {e}")
            return None
    
    def handle_payment_success(self, request, order_sn):
        """处理支付成功"""
        try:
            order = Order.objects.get(order_sn=order_sn, user=request.user)
            if order.status == 'pending':
                order.status = 'paid'
                order.paid_at = timezone.now()
                order.save()
        except Order.DoesNotExist:
            pass
        
        return HttpResponseRedirect('/users/orders/')


class OrderCreateView(LoginRequiredMixin, View):
    """创建订单视图"""
    
    def post(self, request):
        item_id = request.POST.get('item_id')
        item_type = request.POST.get('item_type')
        quantity = int(request.POST.get('quantity', 1))
        contact_name = request.POST.get('contact_name', '')
        contact_phone = request.POST.get('contact_phone', '')
        
        payment_view = OrderPaymentView()
        order = payment_view.create_order(request.user, item_id, item_type, quantity, contact_name, contact_phone)
        
        if order:
            return HttpResponseRedirect(f'/orders/payment/{order.order_sn}/')
        else:
            return JsonResponse({'status': 'error', 'message': '订单创建失败'})


class OrderDetailView(LoginRequiredMixin, TemplateView):
    """订单详情视图"""
    template_name = "orders/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_sn = kwargs.get('order_sn')
        
        # 获取订单，确保是当前用户的订单
        order = get_object_or_404(
            Order.objects.select_related('user').prefetch_related('details'),
            order_sn=order_sn,
            user=self.request.user
        )
        
        context['order'] = order
        context['page_title'] = f'订单详情 - {order.order_sn}'
        
        # 获取订单明细关联的对象信息
        detail_list = []
        for detail in order.details.all():
            detail_data = {
                'detail': detail,
                'item': None,
                'item_url': None,
            }
            
            # 根据item_type获取对应的对象
            if detail.item_type == 'scenic':
                try:
                    item = ScenicSpot.objects.get(pk=detail.item_id)
                    detail_data['item'] = item
                    detail_data['item_url'] = reverse('scenic:detail', kwargs={'pk': detail.item_id})
                except ScenicSpot.DoesNotExist:
                    pass
            elif detail.item_type == 'route':
                try:
                    item = Route.objects.get(pk=detail.item_id)
                    detail_data['item'] = item
                    detail_data['item_url'] = reverse('routes:detail', kwargs={'pk': detail.item_id})
                except Route.DoesNotExist:
                    pass
            elif detail.item_type == 'hotel':
                try:
                    item = Hotel.objects.get(pk=detail.item_id)
                    detail_data['item'] = item
                    detail_data['item_url'] = reverse('hotels:detail', kwargs={'pk': detail.item_id})
                except Hotel.DoesNotExist:
                    pass
            
            detail_list.append(detail_data)
        
        context['detail_list'] = detail_list
        return context


class OrderReviewView(LoginRequiredMixin, View):
    """订单评价跳转视图 - 跳转到订单中第一个项目的详情页进行评价"""
    
    def get(self, request, order_sn):
        # 获取订单，确保是当前用户的订单
        order = get_object_or_404(
            Order,
            order_sn=order_sn,
            user=request.user
        )
        
        # 获取订单的第一个明细
        first_detail = order.details.first()
        if not first_detail:
            return HttpResponseRedirect('/users/orders/')
        
        # 根据item_type跳转到对应的详情页
        if first_detail.item_type == 'scenic':
            return HttpResponseRedirect(reverse('scenic:detail', kwargs={'pk': first_detail.item_id}))
        elif first_detail.item_type == 'route':
            return HttpResponseRedirect(reverse('routes:detail', kwargs={'pk': first_detail.item_id}))
        elif first_detail.item_type == 'hotel':
            return HttpResponseRedirect(reverse('hotels:detail', kwargs={'pk': first_detail.item_id}))
        else:
            return HttpResponseRedirect(reverse('users:orders'))