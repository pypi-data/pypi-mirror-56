# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import json, os, random

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, reverse, redirect, render, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum, Count

from qiniu import Auth
from qiniu import BucketManager

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from dss.Serializer import serializer

from .models import Course, Section, Part, Video, Question, Option, UserCourse, UserSection, \
    UserPart, UserVideo, UserQuestion, UserPartNote
from .forms import CourseForm, SectionForm, PartForm, PartUpdateForm, VideoForm, QuestionForm, \
    QuestionSearchForm, OptionForm, UploadImageForm, UserCourseForm, UserPartNoteForm, UserPartSearchForm
from .utils import page_it, get_user_name_field
from . import signals
from qiniu_api import get_qiniu_token
from qiniu_api import get_video_str as get_qiniu_video_str

User = get_user_model()


# Create your views here.
def test(request):
    q = Question.objects.all()
    for i in q:
        i.course = i.part.section.course
        i.section = i.part.section
        i.save()
    return


# =======course=======
class CourseList(ListView):
    template_name = 'bee_django_course_simple/course/course_list.html'
    context_object_name = 'course_list'
    paginate_by = 20
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('bee_django_course_simple.view_all_courses'):
            self.queryset = Course.objects.none()
        return super(CourseList, self).get(request, *args, **kwargs)


class CourseDetail(DetailView):
    model = Course
    template_name = 'bee_django_course_simple/course/course_detail.html'
    context_object_name = 'course'


@method_decorator(permission_required('bee_django_course_simple.add_course'), name='dispatch')
class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'bee_django_course_simple/course/course_form.html'


class CourseUpdate(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'bee_django_course_simple/course/course_form.html'


class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class SectionList(ListView):
    template_name = 'bee_django_course_simple/section/section_list.html'
    context_object_name = 'section_list'
    paginate_by = 20
    queryset = Section.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("bee_django_course.view_all_sections"):
            return super(SectionList, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        section_name = self.request.GET.get('section_name')
        if section_name:
            return self.queryset.filter(name__contains=section_name)
        else:
            return self.queryset


class SectionDetail(DetailView):
    model = Section
    template_name = 'bee_django_course_simple/section/section_detail.html'
    context_object_name = 'section'


class SectionCreate(CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'bee_django_course_simple/section/section_form.html'

    def get_context_data(self, **kwargs):
        context = super(SectionCreate, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs["course_id"])
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.course_id = self.kwargs["course_id"]
        return super(SectionCreate, self).form_valid(form)


class SectionUpdate(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'bee_django_course_simple/section/section_form.html'

    def get_context_data(self, **kwargs):
        context = super(SectionUpdate, self).get_context_data(**kwargs)
        section = Section.objects.get(id=self.kwargs["pk"])
        context['course'] = section.course
        context['type'] = 'update'
        return context


class SectionDelete(DeleteView):
    model = Section
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class PartList(ListView):
    template_name = 'bee_django_course_simple/part/part_list.html'
    context_object_name = 'part_list'
    paginate_by = 20
    queryset = Part.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("bee_django_course_simple.view_all_parts"):
            return super(PartList, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

            # def get_queryset(self):
            #     section_name = self.request.GET.get('section_name')
            #     if section_name:
            #         return self.queryset.filter(name__contains=section_name)
            #     else:
            #         return self.queryset


class PartDetail(DetailView):
    model = Part
    template_name = 'bee_django_course_simple/part/part_detail.html'
    context_object_name = 'part'


class PartCreate(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'bee_django_course_simple/part/part_form.html'
    part = None

    def get_context_data(self, **kwargs):
        context = super(PartCreate, self).get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs["section_id"])
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.section_id = self.kwargs["section_id"]
        self.part = form.instance
        return super(PartCreate, self).form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.POST:
            if self.part.type == 1:
                return reverse_lazy("bee_django_course_simple:video_add", kwargs={'part_id': self.part.id})
            elif self.part.type == 2:
                return reverse_lazy("bee_django_course_simple:question_add", kwargs={'part_id': self.part.id})
        else:
            return reverse_lazy("bee_django_course_simple:section_detail", kwargs={'pk': self.part.section.id})


class PartUpdate(UpdateView):
    model = Part
    form_class = PartUpdateForm
    template_name = 'bee_django_course_simple/part/part_form.html'
    part = None

    def get_context_data(self, **kwargs):
        context = super(PartUpdate, self).get_context_data(**kwargs)
        part = Part.objects.get(id=self.kwargs["pk"])
        context['section'] = part.section
        context['type'] = 'update'
        return context

    def form_valid(self, form):
        self.part = form.instance
        return super(PartUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bee_django_course_simple:section_detail', kwargs={'pk': self.part.section.id})


class PartDelete(DeleteView):
    model = Part
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


def uptoken(request):
    key = request.GET.get('key')
    token = get_qiniu_token(key)
    if hasattr(settings, "QINIU_CONFIG"):
        domain = settings.QINIU_CONFIG.domain
    else:
        domain = None

    return JsonResponse(data={
        'uptoken': token,
        'domain': domain,
    })


def add_video_to_part(request, part_id):
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        try:
            part = get_object_or_404(Part, pk=part_id)
            video_count = part.video_set.all().count() + 1
            part.video_set.create(file_name=file_name, number=video_count)

            return JsonResponse(data={
                'rc': 0,
                'message': '创建成功'
            })
        except Part.DoesNotExist:
            return JsonResponse(data={
                'rc': -1,
                'message': '未找到对应小节'
            })


# 编辑小节视频的文字
def edit_video_content(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == "POST":
        form = VideoForm(data=request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect(reverse('bee_django_course_simple:part_detail', kwargs={'pk': video.part.id}))
        else:
            pass
    else:
        form = VideoForm(instance=video)

    return render(request, 'bee_django_course_simple/video/video_form.html', context={
        'form': form,
    })


# 视频内容富文本图片上传
@csrf_exempt
def upload_image(request):
    max_size = settings.COURSE_UPLOAD_MAXSIZE
    if request.method == "POST":
        file = request.FILES.get(settings.COURSE_SIMPLE_ATTACH_FILENAME)
        if file.size > max_size:
            return HttpResponse("error|图片大小超过5M!")

        # 保存图片。用户上传的图片，与用户的对应关系也保存到数据库中
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            if request.user.is_authenticated:
                user_image.user = request.user
            user_image.save()
            return HttpResponse(user_image.image.url)
        else:
            print form.errors
            return HttpResponse("error|文件存储错误")
    else:
        return HttpResponse("error|请求错误")


def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    return render(request, 'bee_django_course_simple/video/video_detail.html', context={
        'video': video,
        'url': get_qiniu_video_str(video.file_name)
    })


def delete_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, pk=video_id)

        if request.user.has_perm('bee_django_course_simple.change_section'):
            video.delete()
            return JsonResponse(data={
                'rc': 0,
                'message': '删除成功'
            })
        else:
            return JsonResponse(data={
                'rc': -1,
                'message': '权限不足'
            })


# ========== 小节为问题==============
class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'bee_django_course_simple/question/question_form.html'
    question = None

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs)
        context['part'] = Part.objects.get(id=self.kwargs["part_id"])
        return context

    def form_valid(self, form):
        form.instance.part_id = self.kwargs["part_id"]
        part = Part.objects.get(id=self.kwargs["part_id"])
        form.instance.section_id = part.section.id
        form.instance.course_id = part.section.course.id
        self.question = form.instance
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("bee_django_course_simple:option_add", kwargs={"question_id": self.question.id})


# =======选择题==========
class QuestionList(ListView):
    template_name = 'bee_django_course_simple/question/question_list.html'
    context_object_name = 'question_list'
    paginate_by = 20
    http_method_names = [u'get', u"post"]
    queryset = Question.objects.all()

    def search(self):
        course_id = self.request.GET.get("course")
        section_id = self.request.GET.get("section")
        title = self.request.GET.get("title")

        # 检查权限
        if not self.request.user.has_perm("bee_django_course_simple.view_question"):
            self.queryset = Question.objects.none()
            return self.queryset

        if not course_id in ["", 0, None, "0"]:
            self.queryset = self.queryset.filter(part__section__course__id=course_id)
        if not section_id in ["", 0, None, "0"]:
            self.queryset = self.queryset.filter(part__section__id=section_id)
        if not title in ["", 0, None]:
            self.queryset = self.queryset.filter(title__icontains=title)

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        course_id = self.request.GET.get("course")
        section_id = self.request.GET.get("section")
        title = self.request.GET.get("title")

        context['search_form'] = QuestionSearchForm(
            {"course": course_id, "section": section_id, "title": title})
        return context

    def get(self, request, *args, **kwargs):
        self.queryset = self.search()
        return super(QuestionList, self).get(request, *args, **kwargs)


class UserPartList(ListView):
    template_name = 'bee_django_course_simple/part/user_part_list.html'
    context_object_name = 'user_part_list'
    paginate_by = 20

    def get_name(self):
        user_id = self.request.GET.get("user_id")
        if user_id:
            user = User.objects.get(pk=user_id)

            return user.get_user_name()
        else:
            name = self.request.GET.get("name")
            return name

    def get_context_data(self, **kwargs):
        context = super(UserPartList, self).get_context_data(**kwargs)
        name = self.get_name()
        course = self.request.GET.get("course")
        part = self.request.GET.get("part")
        context['search_form'] = UserPartSearchForm({"name": name, "course": course, "part": part})
        return context

    def get_queryset(self):
        q = UserPart.objects.filter(part__type=2, status=2, part__award_name__isnull=False).order_by('-passed_at')
        user_id = self.request.GET.get("user_id")
        name = self.get_name()
        course = self.request.GET.get("course")
        part = self.request.GET.get("part")
        if not user_id in ["0", 0, None]:
            q = q.filter(user_section__user_course__user=user_id)

        if not name in ["", 0, None]:
            try:
                kwargs = {}  # 动态查询的字段
                name_field = get_user_name_field()
                if name_field:
                    kwargs["user_section__user_course__user__" + name_field + '__icontains'] = name
                    q = q.filter(**kwargs)
            except:
                pass

        if not course in ["0", 0, None]:
            q = q.filter(user_section__user_course__course=course)
        if not part in ["0", 0, None]:
            q = q.filter(part__title__icontains=part)
        return q


class UserPartDetail(DetailView):
    model = UserPart
    template_name = 'bee_django_course_simple/part/user_part_detail.html'
    context_object_name = 'user_part'


class QuestionDetail(DetailView):
    model = Question
    template_name = 'bee_django_course_simple/question/question_detail.html'
    context_object_name = 'question'


class QuestionRecordDetail(DetailView):
    model = Question
    template_name = 'bee_django_course_simple/question/question_reocrd_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionRecordDetail, self).get_context_data(**kwargs)
        question_id = self.kwargs["pk"]
        question = Question.objects.get(id=question_id)
        option_list = Option.objects.filter(question=question)
        res_queryset = UserQuestion.objects.filter(question=question).values('answer_option_id').annotate(
            answer_count=Count('answer_option')).order_by("-answer_count")

        res_list = []
        user_count = 0
        for option in option_list:
            d = {}
            found = False
            for i in res_queryset:
                answer_option_id = i["answer_option_id"]
                if not answer_option_id:
                    found = False
                elif option.id == answer_option_id:
                    d["key"] = option.title
                    d["value"] = i["answer_count"]
                    user_count += i["answer_count"]
                    found = True
                    res_list.append(d)
            if found == False:
                d["key"] = option.title
                d["value"] = 0
                res_list.append(d)

        # for res_dict in res_queryset:
        #     # option_id = res_dict["answer"]
        #     count = res_dict["answer_count"]

        context["user_count"] = user_count
        context["res_list"] = res_list
        # context["res_queryset"]=res_queryset
        return context


class QuestionUpdate(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'bee_django_course_simple/question/question_form.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs["pk"])
        context['part'] = question.part
        return context

    def get_success_url(self):
        question = Question.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("bee_django_course_simple:part_detail", kwargs={"pk": question.part.id})


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class OptionCreate(CreateView):
    model = Option
    form_class = OptionForm
    template_name = 'bee_django_course_simple/question/option_form.html'
    question = None

    def get_context_data(self, **kwargs):
        context = super(OptionCreate, self).get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs["question_id"])
        context['question'] = question
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.question_id = self.kwargs["question_id"]
        self.question = form.instance.question
        return super(OptionCreate, self).form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.POST:
            return reverse_lazy("bee_django_course_simple:option_add", kwargs=self.kwargs)
        else:
            return reverse_lazy("bee_django_course_simple:section_detail", kwargs={"pk": self.question.part.section.id})


class OptionUpdate(UpdateView):
    model = Option
    form_class = OptionForm
    template_name = 'bee_django_course_simple/question/option_form.html'

    def get_context_data(self, **kwargs):
        context = super(OptionUpdate, self).get_context_data(**kwargs)
        option = Option.objects.get(id=self.kwargs["pk"])
        context['question'] = option.question
        context['type'] = 'update'
        return context

    def get_success_url(self):
        option = Option.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("bee_django_course_simple:part_detail", kwargs={"pk": option.question.part.id})


class OptionDelete(DeleteView):
    model = Option
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# ========用户课件列表=========

# 给用户添加新课程
class UserCourseCreate(CreateView):
    model = UserCourse
    form_class = UserCourseForm
    template_name = 'bee_django_course_simple/course/user_course_form.html'
    user_course = None

    # def get_context_data(self, **kwargs):
    #     context = super(OptionCreate, self).get_context_data(**kwargs)
    #     question = Question.objects.get(id=self.kwargs["question_id"])
    #     context['question'] = question
    #     context['type'] = 'add'
    #     return context
    #
    def form_valid(self, form):
        form.instance.user_id = self.kwargs["user_id"]
        self.user_course = form.instance
        return super(UserCourseCreate, self).form_valid(form)

    #
    def get_success_url(self):
        return reverse_lazy("bee_django_course_simple:user_section_list",
                            kwargs={"user_id": self.kwargs["user_id"], "user_course_id": self.user_course.id})


class UserCourseDelete(DeleteView):
    model = UserCourse
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# 查看指定用户user的课件列表
class UserSectionList(ListView):
    template_name = "bee_django_course_simple/section/user_section_list.html"
    model = UserSection
    queryset = None
    paginate_by = 30
    context_object_name = 'user_section_list'
    user_course = None
    user_course_list = None

    def get_section_type_list(self):
        return [1, 2]  # 展示全部课件

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_course_id = self.kwargs["user_course_id"]
        self.user_course_list = UserCourse.objects.filter(user__id=user_id).order_by('status', '-created_at')
        if not user_course_id in [None, 0, "0", u"0"]:
            self.user_course = UserCourse.objects.get(id=user_course_id)
        else:
            if self.user_course_list.exists():
                self.user_course = self.user_course_list.first()
        if self.user_course:
            return UserSection.objects.filter(user_course=self.user_course).filter(
                section__type__in=self.get_section_type_list())
        else:
            return UserSection.objects.none()

    def get_context_data(self, **kwargs):
        context = super(UserSectionList, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["user_id"])
        context["user"] = user
        context["user_course"] = self.user_course
        context["user_course_list"] = self.user_course_list
        return context


class UserSectionDetail(DetailView):
    model = UserSection
    template_name = 'bee_django_course_simple/section/user_section_detail.html'
    context_object_name = 'user_section'


# ======学生前台页面========

class CustomUserSectionRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_id = self.kwargs['user_id']
        section_type = self.kwargs['section_type']
        page_type = self.kwargs['page_type']

        user_course_list = UserCourse.objects.filter(user__id=user_id).order_by('-created_at', "status")
        if user_course_list.exists():
            user_course = user_course_list.first()
            user_section_list = user_course.usersection_set.filter(status__gte=1, section__type=section_type).order_by(
                "status", "section__number")
            if user_section_list.exists():
                user_section = user_section_list.first()
                if page_type == 'detail':
                    self.url = reverse('bee_django_course_simple:custom_user_section_detail',
                                       kwargs={"pk": user_section.id, "section_type": section_type})
                elif page_type == 'list':
                    self.url = reverse('bee_django_course_simple:custom_user_section_list',
                                       kwargs={"section_type": section_type, "user_course_id": user_course.id,
                                               "user_id": user_id})

            else:
                self.url = reverse('bee_django_course_simple:custom_user_section_empty')

                # print('====', self.url)
        else:
            self.url = reverse('bee_django_course_simple:custom_user_section_empty')

        return super(CustomUserSectionRedirect, self).get_redirect_url(*args, **kwargs)


# 普通课件列表，或预备课列表
class CustomUserSectionList(UserSectionList):
    def get_section_type_list(self):
        return [self.kwargs["section_type"]]

    def get_template_names(self):
        section_type = self.kwargs["section_type"]
        if section_type in [1, "1"]:
            return "bee_django_course_simple/section/custom_user_section_list1.html"
        elif section_type in [2, "2"]:
            return "bee_django_course_simple/section/custom_user_section_list2.html"

    def get_context_data(self, **kwargs):
        context = super(CustomUserSectionList, self).get_context_data(**kwargs)
        context["section_type"] = self.kwargs["section_type"]
        return context


class CustomUserSectionDetail(UserSectionDetail):
    def get_template_names(self):
        section_type = self.kwargs["section_type"]
        if section_type in [1, "1"]:
            return 'bee_django_course_simple/section/custom_user_section_detail1.html'
        elif section_type in [2, "2"]:
            return "bee_django_course_simple/section/custom_user_section_detail2.html"

    def get_context_data(self, **kwargs):
        context = super(CustomUserSectionDetail, self).get_context_data(**kwargs)
        user_section = UserSection.objects.get(id=self.kwargs["pk"])
        context["user_section"] = user_section
        context["next_user_section"] = user_section.next_user_section()
        context["section_type"] = self.kwargs["section_type"]
        return context


class CustomUserSectionEmpty(TemplateView):
    template_name = 'bee_django_course_simple/section/custom_user_section_empty.html'


class CustomUserPartDetail(DetailView):
    model = UserPart
    context_object_name = 'user_part'

    def get_context_data(self, **kwargs):
        context = super(CustomUserPartDetail, self).get_context_data(**kwargs)
        user_part = UserPart.objects.get(id=self.kwargs["pk"])
        next_user_part = user_part.next_user_part()
        if user_part.is_pass() and next_user_part:
            context["next_user_part_btn"] = True
        else:
            context["next_user_part_btn"] = False
        if hasattr(settings, "QINIU_CONFIG"):
            domain = settings.QINIU_CONFIG.domain
        else:
            domain = None
        context["qiniu_domain"] = domain
        context["next_user_part"] = user_part.next_user_part()
        return context


class CustomUserPartList(UserPartList):
    template_name = 'bee_django_course_simple/part/custom_user_part_list.html'

    def get_context_data(self, **kwargs):
        context = super(CustomUserPartList, self).get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.request.GET.get("user_id"))
        return context


class CustomUserPartDetailVideo(CustomUserPartDetail):
    template_name = 'bee_django_course_simple/part/custom_user_part_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomUserPartDetailVideo, self).get_context_data(**kwargs)
        user_part = UserPart.objects.get(id=self.kwargs['pk'])
        public_notes = UserPartNote.objects.filter(part=user_part.part, is_open=True).order_by('-created_at')
        my_notes = UserPartNote.objects.filter(part=user_part.part, user=self.request.user)
        note_form = UserPartNoteForm()

        context['public_notes'] = page_it(self.request, query_set=public_notes)
        context['my_notes'] = page_it(self.request, query_set=my_notes)
        context['note_form'] = note_form

        return context

    def post(self, request, *args, **kwargs):
        form = UserPartNoteForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            user_part = UserPart.objects.get(id=self.kwargs['pk'])
            note.part = user_part.part
            note.user = request.user
            note.save()
            signals.user_part_note_created.send(sender=CustomUserPartDetailVideo, user_part_note_id=note.id)

            return redirect(
                reverse('bee_django_course_simple:custom_user_part_detail_video', kwargs={'pk': self.kwargs['pk']}))
        else:
            return render(request, 'bee_django_course_simple/part/custom_user_part_detail.html')


class CustomUserPartDetailQuestion(CustomUserPartDetail):
    template_name = 'bee_django_course_simple/part/custom_user_part_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomUserPartDetailQuestion, self).get_context_data(**kwargs)
        user_part = UserPart.objects.get(id=self.kwargs["pk"])
        context["user_answer_list"] = []
        return context


class UserSectionUpdate(TemplateView):
    def post(self, request, *args, **kwargs):
        user_section_id = self.kwargs["user_section_id"]
        type = self.kwargs["type"]
        user_section = UserSection.objects.get(id=user_section_id)
        msg = ''
        if type == 'open':
            user_section._open()
            msg = '开启'
        elif type == 'pass':
            user_section._pass()

            msg = '通过'
        elif type == 'close':
            user_section._close()
            msg = '关闭'
        return JsonResponse(data={
            'rc': 0,
            'message': msg + '成功'
        })
