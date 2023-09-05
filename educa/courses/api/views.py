from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer
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


class CourseEnrollApiView(APIView):
    """Представление для записи пользователей на курсы."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})

