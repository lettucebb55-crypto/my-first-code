from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('home/', views.UserHomeView.as_view(), name='home'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('orders/', views.UserOrdersView.as_view(), name='orders'),
    path('favorites/', views.UserFavoritesView.as_view(), name='favorites'),
    path('reviews/', views.UserReviewsView.as_view(), name='reviews'),

    # 登录、注册页面
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # 使用自定义的 LogoutView（支持GET请求）
    path('logout/', views.LogoutView.as_view(), name='logout'),
]