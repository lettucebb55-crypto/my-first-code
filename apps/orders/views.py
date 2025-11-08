from django.views.generic import TemplateView

class OrderConfirmView(TemplateView):
    template_name = "orders/confirm.html"
    # 预订流程的确认页面
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '订单确认'
        return context

class OrderPaymentView(TemplateView):
    template_name = "orders/payment.html"
    # 支付页面
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '订单支付'
        return context