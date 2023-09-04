from rest_framework import serializers
from courses.models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов курса."""

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модуля курса."""

    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса."""
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules', 'modules']
