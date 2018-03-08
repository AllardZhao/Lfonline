# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/8 10:28'
import re
from django import forms

from operation.models import UserAsk


# # 方法一：直接写form
# class UserAskForm1(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


# 方法二：直接继承将写的model中UserAsk转变成form
class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk      # 指明要转换哪一个
        fields = ['name', 'mobile', 'course_name']    # 指明要转换的字段

    def clean_mobile(self):   # 正则表达式验证mobile
        """
         验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match((mobile)):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid" )