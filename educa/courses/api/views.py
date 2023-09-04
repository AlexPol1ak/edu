from rest_framework import generics
from courses.models import Subject
from courses.api.serializers import SubjectSerializer

class SubjectApiListView(generics.ListAPIView):
    """Представление для отображения всех курсов."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectApiDetailView(generics.RetrieveAPIView):
    """Представление для отображения курса детально."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer