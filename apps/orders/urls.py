from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('confirm/', views.OrderConfirmView.as_view(), name='confirm'),
    path('payment/<str:order_sn>/', views.OrderPaymentView.as_view(), name='payment'),
]