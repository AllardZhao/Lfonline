# _*_ encoding:utf-8 _*_
__author__ = 'Allard'
__date__ = '2018/2/28 16:04'
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0  # 可以控制 默认显示的tab数量


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # get_zj_nums函数也可以添加到列表页只不过不能修改，动态显示
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'add_time']
    ordering = ['-click_nums']    # 在后台管理系统课程页，根据点击数默认倒叙排列
    readonly_fields = ['click_nums']  # 设置某些字段为只读，在后台管理系统不能修改
    list_editable = ['degree', 'desc']  # 在列表页直接就可以修改
    exclude = ['fav_nums']  # 设置某些字段隐藏不显示，这个和上个设置是冲突的某个字段不能同时设置这两个。
    inlines = [LessonInline, CourseResourceInline]   # 将上面的类添加到inline数组完成页面组装。
    refresh_times = [3, 5]  # 设置列表页定时刷新,范围3至5秒
    style_fields = {"detail": "ueditor"}   # 指明某个字段采用的样式
    import_excel = True

    def queryset(self):  # 过滤出不是轮播课程
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:  # 对Excel进行逻辑操作
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {"detail": "ueditor"}

    def queryset(self):   # 过滤出轮播课程
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
