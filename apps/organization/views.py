# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import Course

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 取出所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 授课机构排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 学习人数，课程数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 取出所有城市
        all_ctiys = CityDict.objects.all()

        # 统计课程机构数
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 5表示每页5个数据
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_ctiys": all_ctiys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort

        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 如果不加commit=True,只是数据提交到数据库没有保存
            user_ask = userask_form.save(commit=True)
            # 通过Ajax的异步操作返回JSON数据,content_type指明返回类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # .format(userask_form.errors)
            return HttpResponse('{"status":"fail", "msg":"添加出错"}',  content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 取出所有课程,有外键的可以用
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
        })
