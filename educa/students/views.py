from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from courses.models import Course
from students.froms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """Представление для регистрации студентов."""
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """Представление для зачисления студентов на курс."""
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        self.course.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """Представление для просмотра курсов на которые зачислены студенты."""

    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qr = super().get_queryset()
        return qr.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """Представление для детального отображения курса студента."""
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qr = super().get_queryset()
        return qr.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        course = self.get_object()

        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()

        return context
