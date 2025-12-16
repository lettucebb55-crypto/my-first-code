from django.urls import path
from . import api

# /api/v1/comments/
urlpatterns = [
    path('<int:comment_id>/', api.CommentAPIView.as_view(), name='api-comment-detail'),
    path('', api.CommentAPIView.as_view(), name='api-comment'),
]

