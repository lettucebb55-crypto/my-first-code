from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminIndexView.as_view(), name='index'),
    # path('scenic/list/', views.AdminScenicListView.as_view(), name='scenic-list'),
    # path('scenic/create/', views.AdminScenicCreateView.as_view(), name='scenic-create'),
    # ... 其他管理页面的路由
]