from django.urls import path
from . import api

app_name = 'checkins_api'

urlpatterns = [
    path('', api.CheckInListAPIView.as_view(), name='list'),
    path('create/', api.CheckInCreateAPIView.as_view(), name='create'),
    path('map/', api.CheckInMapAPIView.as_view(), name='map'),
    path('<int:checkin_id>/', api.CheckInDetailAPIView.as_view(), name='detail'),
    path('<int:checkin_id>/delete/', api.CheckInDeleteAPIView.as_view(), name='delete'),
]

