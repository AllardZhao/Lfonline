# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/2/28 14:11'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


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


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 设置列表默认展示列
    search_fields = ['title', 'image', 'url', 'index']  # 添加搜索功能
    list_filter = ['title', 'image', 'url', 'index', 'add_time']   # 筛选数

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # BaseSetting注册
xadmin.site.register(views.CommAdminView, GlobalSetting)
