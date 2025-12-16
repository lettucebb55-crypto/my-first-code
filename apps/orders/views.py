from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.db.models import F
import time
import uuid
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
        
        # 参数验证
        if not item_id or not item_type:
            context['error'] = '缺少必要参数：请选择要预订的项目'
            return context
        
        try:
            quantity = int(self.request.GET.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
        
        contact_name = self.request.GET.get('contact_name', '').strip()
        contact_phone = self.request.GET.get('contact_phone', '').strip()
        booking_date = self.request.GET.get('booking_date', '')
        check_in_date = self.request.GET.get('check_in_date', '')
        check_out_date = self.request.GET.get('check_out_date', '')
        room_type_id = self.request.GET.get('room_type_id')
        
        # 验证必填参数
        missing_params = []
        if not contact_name:
            missing_params.append('联系人姓名')
        if not contact_phone:
            missing_params.append('联系人手机')
        
        # 根据项目类型验证特定参数
        if item_type == 'hotel':
            if not check_in_date:
                missing_params.append('入住日期')
            if not check_out_date:
                missing_params.append('退房日期')
        elif item_type == 'route':
            if not booking_date:
                missing_params.append('出行日期')
        
        if missing_params:
            context['error'] = f'缺少必要参数：{", ".join(missing_params)}'
            return context
        
        context['item_id'] = item_id
        context['item_type'] = item_type
        context['quantity'] = quantity
        context['contact_name'] = contact_name
        context['contact_phone'] = contact_phone
        context['booking_date'] = booking_date
        context['check_in_date'] = check_in_date
        context['check_out_date'] = check_out_date
        context['room_type_id'] = room_type_id
        
        # 获取项目信息
        item = None
        price = 0
        room_type = None
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
                # 如果指定了房间类型ID，使用指定的房间类型
                if room_type_id:
                    try:
                        room_type = RoomType.objects.get(pk=room_type_id, hotel=item, is_available=True)
                        price = room_type.price
                    except RoomType.DoesNotExist:
                        pass
                # 如果没有指定或找不到，使用最低价格的房间
                if not room_type:
                    room_type = RoomType.objects.filter(hotel=item, is_available=True).order_by('price').first()
                    if room_type:
                        price = room_type.price
            except Hotel.DoesNotExist:
                pass
        
        context['item'] = item
        context['room_type'] = room_type
        context['price'] = price
        
        # 计算酒店入住天数和总价
        if item_type == 'hotel' and check_in_date and check_out_date:
            from datetime import datetime
            try:
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
                nights = (check_out - check_in).days
                context['nights'] = nights if nights > 0 else 1
                # 总价 = 单价 × 天数 × 房间数
                context['total'] = price * context['nights'] * quantity
            except:
                context['nights'] = 1
                context['total'] = price * quantity
        else:
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
        check_in_date = request.POST.get('check_in_date', '')
        check_out_date = request.POST.get('check_out_date', '')
        room_type_id = request.POST.get('room_type_id')
        
        if not all([item_id, item_type, contact_name, contact_phone]):
            return JsonResponse({'status': 'error', 'message': '参数不完整'})
        
        # 酒店预订必须提供入住和退房日期
        if item_type == 'hotel':
            if not check_in_date or not check_out_date:
                return JsonResponse({'status': 'error', 'message': '请选择入住和退房日期'})
        
        # 创建订单
        order = self.create_order(request.user, item_id, item_type, quantity, contact_name, contact_phone, check_in_date, check_out_date, room_type_id)
        
        if order:
            return HttpResponseRedirect(f'/orders/payment/{order.order_sn}/')
        else:
            return JsonResponse({'status': 'error', 'message': '订单创建失败'})
    
    def generate_unique_order_sn(self):
        """生成唯一订单号 - 防止并发冲突"""
        max_retries = 10
        for _ in range(max_retries):
            order_sn = f"BD{timezone.now().strftime('%Y%m%d%H%M%S')}{get_random_string(4, '0123456789')}"
            if not Order.objects.filter(order_sn=order_sn).exists():
                return order_sn
            time.sleep(0.01)  # 等待10ms后重试
        
        # 如果还是重复，使用UUID保证唯一性
        return f"BD{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
    
    @transaction.atomic
    def create_order(self, user, item_id, item_type, quantity, contact_name, contact_phone, check_in_date=None, check_out_date=None, room_type_id=None):
        """
        创建订单 - 使用事务和数据库锁保证并发一致性
        解决并发问题：
        1. 使用 @transaction.atomic 保证原子性
        2. 使用 select_for_update() 锁定资源，防止超卖
        3. 使用 F() 表达式进行原子更新
        4. 订单号生成时检查唯一性
        
        参数说明：
        - check_in_date: 酒店入住日期（仅对酒店类型有效）
        - check_out_date: 酒店退房日期（仅对酒店类型有效）
        - room_type_id: 房间类型ID（仅对酒店类型有效）
        """
        try:
            # 生成唯一订单号
            order_sn = self.generate_unique_order_sn()
            
            # 获取项目信息和价格
            item_name = ''
            price = 0
            
            if item_type == 'scenic':
                # 景点门票通常不需要库存控制，直接获取
                item = ScenicSpot.objects.get(pk=item_id)
                item_name = item.name
                price = item.ticket_price
                
            elif item_type == 'route':
                # 路线需要控制成团人数，使用悲观锁防止超卖
                item = Route.objects.select_for_update().get(pk=item_id)
                item_name = item.name
                price = item.price
                
                # 检查剩余名额（在锁保护下）
                available_slots = item.group_size - item.sales_count
                if available_slots < quantity:
                    raise ValueError(f"名额不足，剩余{available_slots}个名额，您需要{quantity}个")
                
                # 原子性更新销售数量（使用F表达式，数据库层面原子操作）
                Route.objects.filter(id=item_id).update(
                    sales_count=F('sales_count') + quantity
                )
                
            elif item_type == 'hotel':
                # 酒店需要控制房间数量
                item = Hotel.objects.select_for_update().get(pk=item_id)
                
                # 如果指定了房间类型ID，使用指定的房间类型
                if room_type_id:
                    try:
                        room_type = RoomType.objects.select_for_update().get(
                            pk=room_type_id, 
                            hotel=item, 
                            is_available=True
                        )
                    except RoomType.DoesNotExist:
                        raise ValueError("选择的房间类型不存在或不可用")
                else:
                    # 如果没有指定，使用最低价格的房间
                    room_type = RoomType.objects.filter(
                        hotel=item, 
                        is_available=True
                    ).order_by('price').first()
                
                if not room_type:
                    raise ValueError("暂无可用房间")
                
                # 组合酒店名称和房间类型名称
                item_name = f"{item.name} - {room_type.name}"
                price = room_type.price
                
                # 计算酒店入住天数
                if check_in_date and check_out_date:
                    from datetime import datetime
                    try:
                        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
                        nights = (check_out - check_in).days
                        if nights <= 0:
                            raise ValueError("退房日期必须晚于入住日期")
                        # 总价 = 单价 * 天数 * 房间数
                        total_amount = price * nights * quantity
                    except ValueError as e:
                        raise ValueError(f"日期格式错误：{str(e)}")
                    except Exception as e:
                        raise ValueError(f"日期计算错误：{str(e)}")
                else:
                    # 如果没有提供日期，默认1晚
                    total_amount = price * quantity
                
                # 这里可以添加房间库存控制逻辑
                # 例如：RoomType.objects.filter(id=room_type.id).update(available_count=F('available_count') - quantity)
                
            else:
                raise ValueError("不支持的项目类型")
            
            if item_type != 'hotel':
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
            order_detail = OrderDetail.objects.create(
                order=order,
                item_type=item_type,
                item_id=item_id,
                item_name=item_name,
                price=price,
                quantity=quantity,
                subtotal=total_amount
            )
            
            # 如果是酒店预订，保存入住和退房日期
            if item_type == 'hotel' and check_in_date and check_out_date:
                from datetime import datetime
                try:
                    order_detail.check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                    order_detail.check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
                    order_detail.save()
                except:
                    pass  # 如果日期格式错误，忽略但不影响订单创建
            
            return order
            
        except ValueError as e:
            # 业务逻辑错误（如名额不足），直接抛出
            raise
        except Exception as e:
            # 其他错误，记录日志并抛出
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"创建订单失败: {e}", exc_info=True)
            raise ValueError(f"订单创建失败：{str(e)}")
    
    @transaction.atomic
    def handle_payment_success(self, request, order_sn):
        """
        处理支付成功 - 防止重复支付
        使用事务和原子更新保证并发一致性
        """
        try:
            # 使用 select_for_update 锁定订单，防止并发支付
            order = Order.objects.select_for_update().get(
                order_sn=order_sn,
                user=request.user
            )
            
            # 检查订单状态
            if order.status != 'pending':
                # 订单已经不是待支付状态，可能是重复支付，直接跳转
                return HttpResponseRedirect('/users/orders/')
            
            # 原子性更新订单状态（只有pending状态才能更新为paid）
            # 这样可以防止重复支付：如果订单已经被其他请求支付，这个更新会失败（updated=0）
            updated = Order.objects.filter(
                order_sn=order_sn,
                status='pending'  # 只有pending状态才能更新
            ).update(
                status='paid',
                paid_at=timezone.now()
            )
            
            if updated == 0:
                # 订单状态已被其他请求修改（可能已经支付），直接跳转
                return HttpResponseRedirect('/users/orders/')
            
        except Order.DoesNotExist:
            # 订单不存在，跳转到订单列表
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
                'nights': None,  # 酒店入住天数
            }
            
            # 如果是酒店预订，计算入住天数
            if detail.item_type == 'hotel' and detail.check_in_date and detail.check_out_date:
                nights = (detail.check_out_date - detail.check_in_date).days
                detail_data['nights'] = nights if nights > 0 else 1
            
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
        
        # 根据item_type跳转到对应的详情页，并添加锚点参数以跳转到评价区域
        if first_detail.item_type == 'scenic':
            url = reverse('scenic:detail', kwargs={'pk': first_detail.item_id})
            return HttpResponseRedirect(f'{url}?review=true#comment-section')
        elif first_detail.item_type == 'route':
            url = reverse('routes:detail', kwargs={'pk': first_detail.item_id})
            return HttpResponseRedirect(f'{url}?review=true#comment-section')
        elif first_detail.item_type == 'hotel':
            url = reverse('hotels:detail', kwargs={'pk': first_detail.item_id})
            return HttpResponseRedirect(f'{url}?review=true#comment-section')
        else:
            return HttpResponseRedirect(reverse('users:orders'))