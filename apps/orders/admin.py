from django.contrib import admin
from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ('item_name', 'price', 'quantity', 'subtotal')  # 详情设为只读
    can_delete = False
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_sn', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')  # 按状态筛选
    search_fields = ('order_sn', 'user__username', 'contact_phone')

    # 允许在列表页直接修改订单状态
    list_editable = ('status',)

    inlines = [OrderDetailInline]