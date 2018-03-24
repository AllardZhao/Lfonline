# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/2 17:34'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    """
    前台数据验证，request=True表示必填字段
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):       # 邮箱注册验证码
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})  # 当输入错误时抛出异常提示


class ForgetForm(forms.Form):      # 找回密码时验证码
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):       # 密码修改
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile      # 指明要转换哪一个
        fields = ['image']    # 指明要转换的字段


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile      # 指明要转换哪一个
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']    # 指明要转换的字段