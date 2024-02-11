from django.db.models.query_utils import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from habits_app.serializers import (HealthHabitRewardSerializer, HealthWithPleasantHabitCreateSerializer,
                                    HealthWithPleasantHabitSerializer, PleasantHabitSerializer)
from rest_framework.permissions import IsAuthenticated
from habits_app.permissions import IsAutor, IsPublicItem
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
    serializer_class = HealthHabitRewardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(
            Q(associated_with=None, is_pleasant=False, user=self.request.user)
            |
            Q(associated_with=None, is_pleasant=False, is_public=True)
        )


class HealthHabitWithPleasantCreateAPIView(CreateAPIView):
    """
    Представление создания полезной привычки с приятной привычкой.
    Признак публичности приятной привычки такой же, как и у полезной привычки.
    """
    serializer_class = HealthWithPleasantHabitCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.associated_with.user = new_habit.user
        new_habit.associated_with.is_public = new_habit.is_public
        new_habit.save()
        new_habit.associated_with.save()


class HealthHabitWithPleasantListAPIView(ListAPIView):
    serializer_class = HealthWithPleasantHabitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(
            Q(associated_with__isnull=False, user=self.request.user)
            |
            Q(associated_with__isnull=False, is_public=True)
        )


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
    serializer_class = PleasantHabitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(
            Q(is_pleasant=True, user=self.request.user)
            |
            Q(is_pleasant=True, is_public=True)
        )


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsAutor | IsPublicItem,)

    def get_object(self):
        obj = super().get_object()
        if obj.is_pleasant:
            self.serializer_class = PleasantHabitSerializer
        elif obj.associated_with is None and not obj.is_pleasant:
            self.serializer_class = HealthHabitRewardSerializer
        elif obj.associated_with:
            self.serializer_class = HealthWithPleasantHabitSerializer
        return obj


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsAutor,)

    def get_object(self):
        obj = super().get_object()
        if obj.associated_with is None and not obj.is_pleasant:
            self.serializer_class = HealthHabitRewardSerializer
        elif obj.associated_with:
            self.serializer_class = HealthWithPleasantHabitCreateSerializer
        elif obj.is_pleasant:
            self.serializer_class = PleasantHabitSerializer
        return obj


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsAutor)
