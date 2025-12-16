from django.urls import path
from . import views

app_name = 'foods'

urlpatterns = [
    path('', views.FoodListView.as_view(), name='list'),
    path('<int:pk>/', views.FoodDetailView.as_view(), name='detail'),
]

