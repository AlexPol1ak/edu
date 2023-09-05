from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """Разрешение предоставляет доступ к курсам пользователям, которые на них зачислены."""
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
