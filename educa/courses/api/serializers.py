from rest_framework import serializers
from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов курса."""
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']
