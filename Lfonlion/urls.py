# _*_ coding:utf-8 _*_
"""Lfonlion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView    # 专门用于处理静态文件
import xadmin
from django.views.static import serve         # 用于处理静态文件

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
from Lfonlion.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),                                                       # 后台管理url
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),                                       # 登录url
    url('^register/$', RegisterView.as_view(), name="register"),                              # 注册url
    url(r'^captcha/', include('captcha.urls')),                                               # 生成验证码
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),      # 邮箱激活
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),                          # 找回密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url设置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程相关url设置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),


]
