from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

from students.froms import CourseEnrollForm
from .forms import ModuleFormSet
from .models import Course, Module, Content, Subject
from django.apps import apps
from django.forms.models import modelform_factory

from .views_mixins import OwnerCourseEditMixin, OwnerCourseMixin


class ManageCourseListView(OwnerCourseMixin, ListView):
    """Представление для отображения всех курсов автора."""
    model = Course
    template_name = 'courses/list.html'
    permission_required = 'courses.view_course'

    def get_queryset(self):
        qr = super().get_queryset()
        return qr.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """Представление для создания курса."""
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """Представление для обновления курса."""
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """Представление для удаления курса."""
    template_name = 'courses/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """Представление для обработки набора форм добавления, удаления, обновления модулей курса. """
    template_name = 'manage/module/formset.html'

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """Представление для создания/обновления контента содержимого курса."""
    module = None
    model = None
    obj = None
    template_name = 'manage/content/form.html'

    def get_model(self, model_name):

        if model_name in ['text', 'video', 'file', 'image']:
            return apps.get_model(app_label='courses', model_name=model_name)

    def get_form(self, model, *args, **kwargs):

        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):

        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                Content.objects.create(module=self.module, item=obj)

            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    """Представление для удаления содержимого модуля."""

    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course_owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_course', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """Представление для отображения модуля."""
    template_name = 'manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Представление получает новый порядок следования модулей курса в JSON и обновляет его."""

    # Для реализации упорядочивания перетаскиванием

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Представление получает новый порядок следования контента модуля в JSON и обновляет его."""

    def post(self, request):
        for id , order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin, View):
    """Представление отображает все доступные курсы и их модули."""
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):

        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)

        all_courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)

            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)

        return self.render_to_response({'subjects': subjects, 'subject': subject, 'courses': courses})



class CourseDetailView(DetailView):
    """Представление для отображения детальной информации курса."""
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context

