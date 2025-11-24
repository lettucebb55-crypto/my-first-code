from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('list/', views.HotelListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.HotelDetailView.as_view(), name='detail'),
]

