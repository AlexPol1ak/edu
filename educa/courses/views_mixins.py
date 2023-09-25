from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from courses.models import Course


class OwnerMixin:
    """Миксин для отображения всех курсов автора."""

    def get_queryset(self):
        """Возвращает набор содержащий все курсы автора."""
        qr = super().get_queryset()
        return qr.filter(owner=self.request.user)


class OwnerEditMixin:
    """Миксин для определения владельца"""

    def form_valid(self, form):
        """Назначает пользователя автором объекта."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """Миксин предоставляет форму создания курса."""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Миксин предоставляет шаблон курса."""
    template_name = 'courses/form.html'
