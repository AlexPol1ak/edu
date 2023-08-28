from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ModuleFormSet
from .models import Course, Module, Content
from django.apps import apps
from django.forms.models import modelform_factory


class OwnerMixin:
    """Миксин для отображения всех курсов автора."""

    def get_queryset(self):
        qr = super().get_queryset()
        return qr.filter(owner=self.request.user)


class OwnerEditMixin:
    """Миксин для определения владельца"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """Миксин предоставляет форму создания курса."""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Миксин предоставляет форму."""
    template_name = 'manage/courses/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """Представление для отображения всех курсов автора."""
    model = Course
    template_name = 'manage/courses/list.html'
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
    template_name = 'manage/courses/delete.html'
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

