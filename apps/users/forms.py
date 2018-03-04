# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/2 17:34'
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """
    前台数据验证，request=True表示必填字段
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcah = CaptchaField(error_messages={"invalid": u"验证码错误"})  # 当输入错误时抛出异常提示
