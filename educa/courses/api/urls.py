from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('subjects/', views.SubjectApiListView.as_view(), name='subject_list'),
    path('subjects/<pk>/', views.SubjectApiDetailView.as_view(), name='subject_detail'),
    path('courses/<pk>/enroll/', views.CourseEnrollApiView.as_view(), name='course_enroll')
]