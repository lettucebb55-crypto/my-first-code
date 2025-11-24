from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    """订单明细内联编辑"""
    model = OrderDetail
    extra = 0
    can_delete = True  # 允许删除订单明细
    fields = ('item_type', 'item_id', 'item_name', 'price', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)  # 小计自动计算，设为只读


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理 - 支持完整的增删改查"""
    list_display = ('order_sn', 'user', 'user_contact', 'total_amount', 'status', 'status_badge', 'item_count', 'created_at', 'paid_at')
    list_display_links = ('order_sn', 'user')
    list_filter = ('status', 'created_at', 'paid_at')
    search_fields = ('order_sn', 'user__username', 'user__email', 'user__phone', 'contact_name', 'contact_phone')
    list_editable = ('status',)  # 允许在列表页直接修改订单状态
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OrderDetailInline]
    
    # 详情页字段分组
    fieldsets = (
        ('订单基本信息', {
            'fields': ('order_sn', 'user', 'status', 'total_amount')
        }),
        ('联系人信息', {
            'fields': ('contact_name', 'contact_phone')
        }),
        ('时间信息', {
            'fields': ('created_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('order_sn', 'created_at', 'paid_at')  # 订单号和时间信息只读
    
    def save_formset(self, request, form, formset, change):
        """保存表单集时自动计算小计"""
        instances = formset.save(commit=False)
        for instance in instances:
            # 自动计算小计
            instance.subtotal = instance.price * instance.quantity
            instance.save()
        formset.save_m2m()
        # 处理删除的对象
        for obj in formset.deleted_objects:
            obj.delete()
    
    def status_badge(self, obj):
        """显示带颜色的状态标签"""
        colors = {
            'pending': 'warning',
            'paid': 'info',
            'completed': 'success',
            'cancelled': 'danger',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "订单状态"
    
    def user_contact(self, obj):
        """显示用户联系方式"""
        return format_html(
            '<div>姓名: {}</div><div>电话: {}</div>',
            obj.contact_name,
            obj.contact_phone
        )
    user_contact.short_description = "联系人信息"
    
    def item_count(self, obj):
        """显示订单项目数量"""
        count = obj.details.count()
        return format_html('<span class="badge bg-primary">{}</span>', count)
    item_count.short_description = "项目数"
    
    # 批量操作
    actions = ['mark_as_paid', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        """批量标记为已支付"""
        from django.utils import timezone
        count = queryset.filter(status='pending').update(status='paid', paid_at=timezone.now())
        self.message_user(request, f"已将 {count} 个订单标记为已支付")
    mark_as_paid.short_description = "标记为已支付"
    
    def mark_as_completed(self, request, queryset):
        """批量标记为已完成"""
        count = queryset.filter(status='paid').update(status='completed')
        self.message_user(request, f"已将 {count} 个订单标记为已完成")
    mark_as_completed.short_description = "标记为已完成"
    
    def mark_as_cancelled(self, request, queryset):
        """批量标记为已取消"""
        count = queryset.filter(status__in=['pending', 'paid']).update(status='cancelled')
        self.message_user(request, f"已将 {count} 个订单标记为已取消")
    mark_as_cancelled.short_description = "标记为已取消"


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    """订单明细独立管理"""
    list_display = ('id', 'order', 'item_type', 'item_name', 'price', 'quantity', 'subtotal')
    list_display_links = ('id', 'order')
    list_filter = ('item_type', 'order__status', 'order__created_at')
    search_fields = ('order__order_sn', 'item_name', 'order__user__username')
    date_hierarchy = 'order__created_at'
    ordering = ('-order__created_at',)
    list_editable = ('price', 'quantity')  # 允许在列表页直接编辑价格和数量
    
    fieldsets = (
        ('订单信息', {
            'fields': ('order',)
        }),
        ('项目信息', {
            'fields': ('item_type', 'item_id', 'item_name', 'price', 'quantity', 'subtotal')
        }),
    )
    
    readonly_fields = ('subtotal',)  # 小计自动计算
    
    def get_readonly_fields(self, request, obj=None):
        """创建时所有字段可编辑，编辑时部分字段只读"""
        if obj:  # 编辑模式
            return self.readonly_fields + ('order', 'item_type', 'item_id')
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """保存时自动计算小计"""
        obj.subtotal = obj.price * obj.quantity
        super().save_model(request, obj, form, change)