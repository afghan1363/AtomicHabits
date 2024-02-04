from rest_framework.generics import CreateAPIView, ListAPIView
from habits_app.serializers import (HealthHabitRewardSerializer, HealthWithPleasantHabitCreateSerializer,
                                    HealthWithPleasantHabitSerializer, PleasantHabitSerializer)
from rest_framework.permissions import IsAuthenticated
from habits_app.models import Habit


class HealthHabitWithRewardCreateAPIView(CreateAPIView):
    """
    Представление создания полезной привычки с вознаграждением
    """
    serializer_class = HealthHabitRewardSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HealthHabitWithRewardListAPIView(ListAPIView):
    queryset = Habit.objects.filter(associated_with=None, is_pleasant=False)
    serializer_class = HealthHabitRewardSerializer
    permission_classes = (IsAuthenticated,)


class HealthHabitWithPleasantCreateAPIView(CreateAPIView):
    """
    Представление создания полезной привычки с приятной привычкой
    """
    serializer_class = HealthWithPleasantHabitCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = new_habit.associated_with.user = self.request.user

        new_habit.save()


class HealthHabitWithPleasantListAPIView(ListAPIView):
    queryset = Habit.objects.filter(reward=None)
    serializer_class = HealthWithPleasantHabitSerializer
    permission_classes = (IsAuthenticated,)


class PleasantHabitCreateAPIView(CreateAPIView):
    """
    Представление создания приятной привычки
    """
    serializer_class = PleasantHabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.is_pleasant = True
        new_habit.save()


class PleasantHabitListAPIView(ListAPIView):
    queryset = Habit.objects.filter(is_pleasant=True)
    serializer_class = PleasantHabitSerializer
    permission_classes = (IsAuthenticated,)
