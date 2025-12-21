from django.urls import path
from . import api

urlpatterns = [
    path('plan/', api.AIPlanAPIView.as_view(), name='api-ai-plan'),
    path('history/', api.AIQueryHistoryAPIView.as_view(), name='api-ai-history'),
    path('query/<int:query_id>/', api.AIQueryDetailAPIView.as_view(), name='api-ai-query-detail'),
    path('query/<int:query_id>/favorite/', api.AIQueryFavoriteAPIView.as_view(), name='api-ai-query-favorite'),
    path('query/<int:query_id>/export/', api.AIQueryExportAPIView.as_view(), name='api-ai-query-export'),
]

