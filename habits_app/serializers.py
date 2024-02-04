from rest_framework.serializers import ModelSerializer
from habits_app.models import Habit


class HealthHabitRewardSerializer(ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('associated_with', 'is_pleasant')


class PleasantHabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        exclude = ('reward', 'associated_with',)


class HealthWithPleasantHabitCreateSerializer(ModelSerializer):
    """
    Сериализатор создания полезной привычки со связанной с нею приятной привычкой
    """
    associated_with = PleasantHabitSerializer()

    class Meta:
        model = Habit
        exclude = ('reward',)

    def create(self, validated_data):
        associated_with = validated_data.pop('associated_with')
        pleasant_habit = Habit.objects.create(**associated_with, is_pleasant=True)
        healthy_habit_item = Habit.objects.create(**validated_data, associated_with=pleasant_habit)
        return healthy_habit_item


class HealthWithPleasantHabitSerializer(ModelSerializer):
    associated_with = PleasantHabitSerializer()

    class Meta:
        model = Habit
        exclude = ('reward',)
