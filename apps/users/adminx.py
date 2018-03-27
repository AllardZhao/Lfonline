# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/2/28 14:11'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row

from .models import EmailVerifyRecord, Banner, UserProfile


class UserProfileAdmin(UserAdmin):    # 使用xadmin自带的用户表useradmin用户表，extra_apps\xadmin\plugins\auth.py
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):
    """
    xadmin全局配置
    """
    enable_themes = True   # 主题功能
    use_bootswatch = True


class GlobalSetting(object):
    """
    修改左上角log和页面下公司
    """
    site_title = "学有后台管理系统"
    site_footer = "学有在线网"
    menu_style = "accordion"  # 左侧导航栏，将一个app中表收起来


class EmailVerifyRecordAdmin(object):    # 注册 验证码表
    list_display = ['code', 'email', 'send_type', 'send_time']   # 设置列表默认展示列
    search_fields = ['code', 'email', 'send_type']  # 添加搜索功能
    list_filter = ['code', 'email', 'send_type', 'send_time']   # 筛选数据
    # xadmin后台管理系统注册表图标，即model_icon
    model_icon = 'fa fa-address-book-o'   # 前面fa是不能变的，fa-address-book-o改变来显示不同图标


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 设置列表默认展示列
    search_fields = ['title', 'image', 'url', 'index']  # 添加搜索功能
    list_filter = ['title', 'image', 'url', 'index', 'add_time']   # 筛选数

# 卸载Xadmin自动注册用户
# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)  # BaseSetting注册
xadmin.site.register(views.CommAdminView, GlobalSetting)
