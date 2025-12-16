from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminIndexView.as_view(), name='index'),
    
    # 景点管理
    path('scenic/', views.ScenicListView.as_view(), name='scenic_list'),
    path('scenic/add/', views.ScenicSpotCreateView.as_view(), name='scenic_add'),
    path('scenic/<int:pk>/edit/', views.ScenicSpotUpdateView.as_view(), name='scenic_edit'),
    path('scenic/<int:pk>/delete/', views.ScenicSpotDeleteView.as_view(), name='scenic_delete'),
    
    # 路线管理
    path('routes/', views.RoutesListView.as_view(), name='routes_list'),
    path('routes/add/', views.RouteCreateView.as_view(), name='route_add'),
    path('routes/<int:pk>/edit/', views.RouteUpdateView.as_view(), name='route_edit'),
    path('routes/<int:pk>/delete/', views.RouteDeleteView.as_view(), name='route_delete'),
    
    # 酒店管理
    path('hotels/', views.HotelsListView.as_view(), name='hotels_list'),
    path('hotels/add/', views.HotelCreateView.as_view(), name='hotel_add'),
    path('hotels/<int:pk>/edit/', views.HotelUpdateView.as_view(), name='hotel_edit'),
    path('hotels/<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel_delete'),
    
    # 资讯管理
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_add'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    
    # 用户管理
    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # 订单管理
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/update-status/', views.OrderUpdateStatusView.as_view(), name='order_update_status'),
    
    # 用户评价管理
    path('comments/', views.CommentsListView.as_view(), name='comments_list'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # 美食管理
    path('foods/', views.FoodsListView.as_view(), name='foods_list'),
    path('foods/add/', views.FoodCreateView.as_view(), name='food_add'),
    path('foods/<int:pk>/edit/', views.FoodUpdateView.as_view(), name='food_edit'),
    path('foods/<int:pk>/delete/', views.FoodDeleteView.as_view(), name='food_delete'),
]
