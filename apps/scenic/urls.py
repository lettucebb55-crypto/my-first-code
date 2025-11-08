from django.urls import path
from . import views

app_name = 'scenic'

urlpatterns = [
    # 页面
    path('list/', views.ScenicListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.ScenicDetailView.as_view(), name='detail'),
]