from rest_framework import generics

from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания пользователя
    """
    serializer_class = UserSerializer
