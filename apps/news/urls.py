from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('list/', views.NewsListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
]