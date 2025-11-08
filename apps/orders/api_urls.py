from django.urls import path
from . import api

# /api/v1/orders/
urlpatterns = [
    path('create/', api.OrderCreateAPIView.as_view(), name='api-create'),
    path('list/', api.OrderListAPIView.as_view(), name='api-list'),
    path('detail/<str:order_sn>/', api.OrderDetailAPIView.as_view(), name='api-detail'),
]