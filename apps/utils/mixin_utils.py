# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/14 14:37'

from django.contrib.auth.decorators import login_required    # 调用django装饰器
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    登录权限的认证，在未登录时不执行相应的View，例如：点击开始学习先进行登录验证，
    未登录状态下，跳转到登录页面进行验证登录。
    """
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
