from rest_framework import generics
from users.serializers import UserSerializer
from users.models import User


class UserCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания пользователя
    """
    serializer_class = UserSerializer

