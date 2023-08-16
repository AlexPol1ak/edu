from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

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


class OwnerCourseMixin(OwnerMixin):
    """Миксин предоставляет форму создания курса."""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Миксин предоствляет форму."""
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """Представление для отображения всех курсов автора."""
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qr = super().get_queryset()
        return qr.filter(owner=self.request.owner)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """Представление для создания курса."""
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """Представление для обновления курса."""
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """Представление для удаления курса."""
    template_name = 'courses/manage/course/delete.html'
