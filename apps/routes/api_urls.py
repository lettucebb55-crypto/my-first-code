from django.urls import path
from . import api

# /api/v1/routes/
urlpatterns = [
    path('categories/', api.RouteCategoryListView.as_view(), name='api-category-list'),
    path('routes/', api.RouteListView.as_view(), name='api-route-list'),
    path('routes/<int:pk>/', api.RouteDetailView.as_view(), name='api-route-detail'),
]