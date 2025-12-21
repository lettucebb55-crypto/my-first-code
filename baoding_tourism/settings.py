"""
Django settings for baoding_tourism project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-YOUR_SECRET_KEY_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # 自定义的应用 (按照apps/目录结构)
    'apps.users',
    'apps.scenic',
    'apps.routes',
    'apps.news',
    'apps.orders',
    'apps.hotels',      # 酒店模块
    'apps.comments',    # 评论模块
    'apps.checkins',    # 打卡签到模块
    'apps.foods',       # 美食文化模块
    'apps.admin_panel', # 自定义后台
    'apps.index',       # 用于处理首页等
    'apps.ai_assistant', # AI助手模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'baoding_tourism.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 告知Django去 'templates' 文件夹中寻找模板
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'baoding_tourism.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # ... (默认)
]

# 指定自定义的用户模型
AUTH_USER_MODEL = 'users.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans' # 设置为中文

TIME_ZONE = 'Asia/Shanghai' # 设置为东八区时间

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# 静态文件访问URL
STATIC_URL = 'static/'
# 静态文件存放目录 (项目根目录下的 'static' 文件夹)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploaded files)
# 用户上传文件的访问URL（必须以/开头和结尾）
MEDIA_URL = '/media/'
# 用户上传文件的存储目录 (项目根目录下的 'media' 文件夹)
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# --- 我们的自定义配置 ---

# 登录相关配置
LOGIN_URL = '/users/login/'  # 未登录用户访问需要登录的页面时重定向到登录页
LOGIN_REDIRECT_URL = '/'  # 登录成功后重定向到首页

# 退出登录后重定向到首页
LOGOUT_REDIRECT_URL = '/'

# 允许使用 GET 请求退出登录
LOGOUT_ON_GET = True

# AI助手配置
# 是否使用真实AI API（False时使用规则引擎）
USE_AI_API = False
# AI服务提供商：'openai', 'qianfan', 'dashscope'
AI_PROVIDER = 'openai'
# OpenAI配置（如果使用OpenAI）
OPENAI_API_KEY = ''  # 从环境变量读取：os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = 'gpt-3.5-turbo'  # 或 'gpt-4'