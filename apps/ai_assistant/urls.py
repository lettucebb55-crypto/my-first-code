from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.AIAssistantView.as_view(), name='index'),
    path('history/', views.AIHistoryView.as_view(), name='history'),
]

