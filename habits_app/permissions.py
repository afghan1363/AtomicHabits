from rest_framework.permissions import BasePermission


class IsAutor(BasePermission):
    message = 'Такое может вытворять только автор привычки.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsPublicItem(BasePermission):
    message = 'Это тайная привычка.'

    def has_object_permission(self, request, view, obj):
        return obj.is_public


class IsOwner(BasePermission):
    message = 'Только для создателя записи'

    def has_permission(self, request, view):
        return request.user == view.get_object().user
