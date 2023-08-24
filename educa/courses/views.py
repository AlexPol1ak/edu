from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ModuleFormSet
from .models import Course


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

    def post(self,request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})
