# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/3/4 16:00'
from random import Random
from django.core.mail import send_mail    # 调用此函数发送邮箱

from users.models import EmailVerifyRecord
from Lfonlion.settings import EMAIL_FORM


def random_str(randomlength=8):     # 生成随机字符串供邮箱验证用
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):    # 邮箱激活实现
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 向用户发送邮件
    email_title = ""
    email_allard = ""
    if send_type == "register":
        email_title = "学友在线网注册激活链接"     # 邮件标题
        email_allard = "请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)    # 邮件正文内容
        # 向用户发送邮件
        send_status = send_mail(email_title, email_allard, EMAIL_FORM, [email])

        if send_status:
            pass
    elif send_type == "forget":
        email_title = "学友在线网密码重置连接"  # 邮件标题
        email_allard = "请点击下面链接激活你的账号：http://127.0.0.1:8000/reset/{0}".format(code)  # 邮件正文内容
        # 向用户发送邮件
        send_status = send_mail(email_title, email_allard, EMAIL_FORM, [email])
        if send_status:     # 测试是否发送成功，如果send_status为True说明已发送成功
            pass
    elif send_type == "update_email":
        email_title = "学友在线网邮箱修改验证码"  # 邮件标题
        email_allard = "你的邮箱验证码为：{0}".format(code)  # 邮件正文内容
        # 向用户发送邮件
        send_status = send_mail(email_title, email_allard, EMAIL_FORM, [email])
        if send_status:  # 测试是否发送成功，如果send_status为True说明已发送成功
            pass
