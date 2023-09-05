from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer, CourseSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

class SubjectApiListView(generics.ListAPIView):
    """Представление для отображения всех курсов."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectApiDetailView(generics.RetrieveAPIView):
    """Представление для отображения курса детально."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollApiView(APIView):
#     """Представление для записи пользователей на курсы."""
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled': True})

class CourseEnrollApiView(APIView):
    """Представление для записи пользователей на курсы."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

class CourseApiViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для чтения курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer