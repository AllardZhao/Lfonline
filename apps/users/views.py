# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password   # 调用此函数对明文进行加密
from django.http import HttpResponse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    """
     登录验证密码登录或邮箱登录,引入Q方法实现变量之间的并\或操作，Q()|Q()或关系，Q()，Q()并操作
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    激活账号字段为is_active至为Trues
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return  render(request, "active_fail.html")  # 链接失效
        return render(request, "login.html")


class RegisterView(View):
    """
    注册页面逻辑代码
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):   # 邮箱注册，user数据保存
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):    # 判断用户是否已经存在
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在！"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False  # 表明用户还没激活，因为默认是1，所以指定为False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """
    登录页面的逻辑代码
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"} )
        else:
            return render(request, "login.html", {"login_form": login_form})

# Create your views here.


# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg": "用户名或密码错误！"})
#     elif request.method == "GET":
#         return render(request, "login.html", {})


class ForgetPwdView(View):
    """
    密码找回
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", '')
            send_register_email(email, "forget")
            return render(request,"send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    """
    密码找回
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")  # 链接失效
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息，继承LoginRequiredMixin表示登录才能访问的View
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头型
    """

    # # 方法一
    # def post(self, request):
    #     image_form = UploadImageForm(request.POST, request.FILES)
    #     if image_form.is_valid():
    #         image = image_form.cleaned_data['image']
    #         request.user.image = image
    #         request.user.save()

    # 方法2:直接通过model_form进行保存
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # 返回JSON数据，在页面通过AJAX进行异步提示
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

