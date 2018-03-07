# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 取出所有课程机构
        all_orgs = CourseOrg.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 统计课程机构数
        org_nums = all_orgs.count()

        # 取出所有城市
        all_ctiys = CityDict.objects.all()
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

        })
