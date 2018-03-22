# coding=utf-8
"""
Django settings for Lfonlion project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# 将apps目录添加到搜索路径之下
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$@pwm%g58zuybyu9$jpkqx9q^wtz&h8#yt2593f=qqj7#gv7x@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 自定义AUTH方法
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# Application definition，app应用注册
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # 如果注释掉我们的自动登录就会失效
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    'xadmin',
    'crispy_forms',
    # 验证码使用的库
    'captcha',
    # 页面分页使用的库
    'pure_pagination',
]
# 重载setting方法
AUTH_USER_MODEL = "users.UserProfile"

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Lfonlion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Lfonlion.wsgi.application'


# Database，数据库设置
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lfonline',
        'USER': "root",
        'PASSWORD': "123456",
        'HOST': "127.0.0.1"
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 显示为中文

TIME_ZONE = 'Asia/shanghai'   # 时区为上海

USE_I18N = True

USE_L10N = True

USE_TZ = False   # 使用本地时间，所以将国际时间改为Fasle


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')
# 设置static文件存放路径的地址配置
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, "static"),
)


# 邮箱验证设置
EMAIL_HOST = "smtp.sina.com"   # 新浪邮箱,SMTP服务器
EMAIL_PORT = 25
EMAIL_HOST_USER = "allardzhao@sina.com"
EMAIL_HOST_PASSWORD = "admin123"    # 此处admin123错误 ，需要改成自己新浪邮箱密码
EMAIL_USE_TLS = False
EMAIL_FORM = "allardzhao@sina.com"

# 上传文件(资源文件)的相关设置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

