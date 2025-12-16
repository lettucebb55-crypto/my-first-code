from django.urls import path
from . import api

app_name = 'foods_api'

urlpatterns = [
    path('', api.FoodListAPIView.as_view(), name='list'),
    path('categories/', api.FoodCategoryListAPIView.as_view(), name='categories'),
    path('<int:food_id>/', api.FoodDetailAPIView.as_view(), name='detail'),
]

