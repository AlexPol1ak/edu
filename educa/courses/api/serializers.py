from rest_framework import serializers
from courses.models import Subject, Course, Module, Content


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


class ItemRelatedField(serializers.RelatedField):
    """Кастомное поле для сериализации контента курса."""

    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для контента."""
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модуля и контента модуля курса."""
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """Сериализатор для курса, модуля, контента."""
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']