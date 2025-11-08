from django.urls import path
from . import api

# /api/v1/news/
urlpatterns = [
    path('categories/', api.NewsCategoryListView.as_view(), name='api-category-list'),
    path('list/', api.NewsListView.as_view(), name='api-list'),
    path('detail/<int:pk>/', api.NewsDetailView.as_view(), name='api-detail'),
    path('detail/<int:pk>/comment/', api.CommentAPIView.as_view(), name='api-comment'),
]