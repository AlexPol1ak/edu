from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', views.CourseApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subjects/', views.SubjectApiListView.as_view(), name='subject_list'),
    path('subjects/<pk>/', views.SubjectApiDetailView.as_view(), name='subject_detail'),
    # path('courses/<pk>/enroll/', views.CourseEnrollApiView.as_view(), name='course_enroll')

]