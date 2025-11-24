from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/', views.CommentCreateView.as_view(), name='create'),
]

