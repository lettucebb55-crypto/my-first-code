from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django 默认后台 (保留, 可选)
    path('admin/', admin.site.urls),

    # 首页
    path('', include('apps.index.urls')),

    # 各模块页面路由
    path('users/', include('apps.users.urls')),
    path('scenic/', include('apps.scenic.urls')),
    path('routes/', include('apps.routes.urls')),
    path('news/', include('apps.news.urls')),
    path('orders/', include('apps.orders.urls')),
    path('admin_panel/', include('apps.admin_panel.urls')), # 自定义后台

    # API 接口路由 (统一前缀 /api/v1/)
    path('api/v1/users/', include('apps.users.api_urls')),
    path('api/v1/scenic/', include('apps.scenic.api_urls')),
    path('api/v1/routes/', include('apps.routes.api_urls')),
    path('api/v1/news/', include('apps.news.api_urls')),
    path('api/v1/orders/', include('apps.orders.api_urls')),
]

# 在开发模式下，允许Django服务静态文件和媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)