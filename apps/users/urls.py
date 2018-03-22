# _*_ coding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/21 14:08'

from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

urlpatterns = [
    # 用户个人信息
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 用户个人中心发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 用户个人中心发送邮箱验证码
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
]