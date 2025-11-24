from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('confirm/', views.OrderConfirmView.as_view(), name='confirm'),
    path('payment/<str:order_sn>/', views.OrderPaymentView.as_view(), name='payment'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('detail/<str:order_sn>/', views.OrderDetailView.as_view(), name='detail'),
    path('review/<str:order_sn>/', views.OrderReviewView.as_view(), name='review'),
]