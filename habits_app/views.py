from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from habits_app.paginators import HabitPaginator
from habits_app.serializers import (HealthWithPleasantHabitCreateSerializer, HabitSerializer)
from rest_framework.permissions import IsAuthenticated
from habits_app.permissions import IsAutor, IsPublicItem, IsOwner
from habits_app.models import Habit


class HabitCreateAPIView(CreateAPIView):
    """
    Представление создания привычки
    """
    serializer_class = HealthWithPleasantHabitCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        if new_habit.associated_with:
            new_habit.associated_with.user = new_habit.user
            new_habit.associated_with.is_public = new_habit.is_public
            new_habit.save()
            new_habit.associated_with.save()
        else:
            new_habit.save()


class SelfHabitListAPIView(ListAPIView):
    """
    Вывод списка своих привычек
    """
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    """
    Вывод списка опубликованных привычек других пользователей
    """
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Просмотр привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsAutor | IsPublicItem,)


class HabitUpdateAPIView(UpdateAPIView):
    """
    Редактирование привычки
    """
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)
    serializer_class = HealthWithPleasantHabitCreateSerializer


class HabitDestroyAPIView(DestroyAPIView):
    """
    Удаление привычки
    """
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsAutor)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'pleasant'):
            self.perform_destroy(instance.pleasant)
        elif instance.associated_with:
            self.perform_destroy(instance.associated_with)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
