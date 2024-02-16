from rest_framework.permissions import BasePermission


class IsAutor(BasePermission):
    """
    Права пользователя на объект
    """
    message = 'Такое может вытворять только автор привычки.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsPublicItem(BasePermission):
    """
    Проверка публичности привычки
    """
    message = 'Это тайная привычка.'

    def has_object_permission(self, request, view, obj):
        return obj.is_public


class IsOwner(BasePermission):
    """
    Права пользователя на контроллер
    """
    message = 'Только для создателя записи'

    def has_permission(self, request, view):
        return request.user == view.get_object().user
