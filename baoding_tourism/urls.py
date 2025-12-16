from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django 默认后台 (已关闭)
    # path('admin/', admin.site.urls),

    # 首页
    path('', include('apps.index.urls')),

    # 各模块页面路由
    path('users/', include('apps.users.urls')),
    path('scenic/', include('apps.scenic.urls')),
    path('routes/', include('apps.routes.urls')),
    path('news/', include('apps.news.urls')),
    path('orders/', include('apps.orders.urls')),
    path('hotels/', include('apps.hotels.urls')),
    path('checkins/', include('apps.checkins.urls')),  # 打卡签到模块
    path('foods/', include('apps.foods.urls')),  # 美食文化模块
    path('admin_panel/', include('apps.admin_panel.urls')),  # 您的自定义统计后台

    # API 接口路由 (统一前缀 /api/v1/)
    path('api/v1/users/', include('apps.users.api_urls')),
    path('api/v1/scenic/', include('apps.scenic.api_urls')),
    path('api/v1/routes/', include('apps.routes.api_urls')),
    path('api/v1/news/', include('apps.news.api_urls')),
    path('api/v1/orders/', include('apps.orders.api_urls')),
    path('api/v1/checkins/', include('apps.checkins.api_urls')),  # 打卡签到API
    path('api/v1/foods/', include('apps.foods.api_urls')),  # 美食文化API
    path('api/v1/comments/', include('apps.comments.api_urls')),  # 评论API
]

# 在开发模式下，允许Django服务静态文件和媒体文件
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)