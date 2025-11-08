from django.urls import path
from . import api

# /api/v1/scenic/
urlpatterns = [
    path('categories/', api.CategoryListView.as_view(), name='api-category-list'),
    path('spots/', api.SpotListView.as_view(), name='api-spot-list'),
    path('spots/<int:pk>/', api.SpotDetailView.as_view(), name='api-spot-detail'),
]