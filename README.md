# Lfonline
> Lfonline 全称 Learn Friend online，是一款在线教育学习平台。

#### 简介
* 学友在线教育学习平台解决主要问题是学习资源获取困难、教学资源分配不均、学习成本高昂。整合各种机构资源使人们更容易的学习到知识，由于纸质书本和机构培训的成本问题此平台的出现降低人们的学习成本。相对于发达地区获取资源比欠发达地区更容易此平台的出现可以更好解决资源分配不均问题。
    
#### 功能介绍
* 1.学友教育平台分分为学友后台管理系统和学友在线教育系统。
* 2.学友后台管理系统主要是对数据表进行管理。设计的管理员权限最大可以对所有数据表进行增删改查，可以对用户操作进行必要设置。
* 3.学友在线教育系统主要分为四个模块：用户模块、课程模块、机构模块、用户操作模块。
  - (1)用户模块实现注册、登录、找回密码、个人中心等。
  - (2)课程模块实现课程分页、热门排行、进入课程查看详情、点击学习观看课程等。
  - (3)机构模块实现机构分页，进入机构可以查看机构详情，机构的课程。
  - (4)用户操作模块实现首页的全局搜索功能、邮箱注册并激活
      
#### 项目描述

* 该项目是个网上技术学习平台，分为学友后台管理系统和学友在线教育系统。学友后台管系统：设有管理员和普通用户权限。管理员权限最大可以查看所有数据信息，设置普通用户可以查看内容权限，可以对所有数据进行增删改查，普通用户可以查看到管理员设置给该用户查看内容。学友在线教育系统：用户注册登录可以查看所有公开课、授课机构、授课讲师。公开课可以查看所有课程、课程详细信息、播放课程内容。授课讲师可以查看所有讲师、讲师详细信息、人气排名查看优秀讲师。授课机构可以查看所有机构、查看机构的详细信息机构课程机构讲师。
    
#### 技术实现：
- 1、通过startapp创建course公开课模块，在models.py通过继承django.db的models.Model来创建需要的数据表，使用migrate来生成数据库中数据表。
- 2、这个项目使用开源的xadmin后台管理系统，因此在course的app新建xadmin.py文件通过xadmin.site.register向后台管理系统注册数据表。
- 3、前台页面显示采用Django模板引擎实现，通过定义一个基类HTML页面用来页面的继承，采用标签for来遍历动态展示信息，分页通过开源django-pure-pagination库来更易操作进行课程分页展示。

#### 公开课views逻辑处理界面

```
# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin     # 引入登录权限的基础类

# Create your views here.


class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        # 因为默认排序是最新所以要按添加时间倒序排列
        all_courses = Course.objects.all().order_by("-add_time")

        # 根据点击数进行热门排序,取3个
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索，通过AJAX进行异步操作，代码在deco-common.js中
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 例如name__icontains为搜索name字段,通过这种操作就可以实现like查询，contains前面的i表示不区分大小写。
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords) |
                Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 6表示每页6个数据
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        # 相关课程推荐功能实现
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其它的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 课程推荐操作
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []

        return render(request, "course-detail.html", {
            "course": course,
            "relate_course": relate_course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        # 相关课程推荐功能实现
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其它的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 相关课程推荐功能实现
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其它的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        # 自己改过的亮点
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
```
