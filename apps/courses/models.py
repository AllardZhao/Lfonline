# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg

# Create your models here.


class Course(models.Model):
    """
    课程基本信息
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True )
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(verbose_name=u"难度", choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name=u"课程类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def get_learn_user(self):
        # 获取学习课程用户
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson (models.Model):
    """
    章节信息，通过外建关联Course
    """
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name


class Video(models.Model):
    """
    视频信息，通过外建关联Lesson
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    """
     课程资源通过外键关联Course
    """
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
