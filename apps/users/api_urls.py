from django.urls import path
from . import api

# /api/v1/users/
urlpatterns = [
    path('register/', api.RegisterAPIView.as_view(), name='api-register'),
    path('login/', api.LoginAPIView.as_view(), name='api-login'),
    path('profile/', api.ProfileAPIView.as_view(), name='api-profile'),
    path('favorites/', api.FavoriteAPIView.as_view(), name='api-favorites'),
]