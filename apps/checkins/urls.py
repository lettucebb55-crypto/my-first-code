from django.urls import path
from . import views

app_name = 'checkins'

urlpatterns = [
    path('list/', views.CheckInListView.as_view(), name='list'),
    path('map/', views.CheckInMapView.as_view(), name='map'),
    path('create/<int:scenic_spot_id>/', views.CheckInCreateView.as_view(), name='create'),
]

