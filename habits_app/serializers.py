from rest_framework.serializers import ModelSerializer, IntegerField
from habits_app.models import Habit
from habits_app.validators import ValidPost, ValidPleasantHabit


class HealthHabitRewardSerializer(ModelSerializer):
    id = IntegerField(read_only=True)

    class Meta:
        model = Habit
        exclude = ('associated_with', 'is_pleasant')
        validators = (ValidPost(fields=exclude),)


class PleasantHabitSerializer(ModelSerializer):
    id = IntegerField(read_only=True)

    class Meta:
        model = Habit
        exclude = ('reward', 'associated_with',)
        validators = (ValidPost(fields=exclude),)


class HealthWithPleasantHabitCreateSerializer(ModelSerializer):
    """
    Сериализатор создания полезной привычки со связанной с нею приятной привычкой
    """
    id = IntegerField(read_only=True)
    associated_with = PleasantHabitSerializer()

    class Meta:
        model = Habit
        exclude = ('reward',)
        validators = (ValidPost(fields=exclude), ValidPleasantHabit(),)

    def create(self, validated_data):
        associated_with = validated_data.pop('associated_with')
        pleasant_habit = Habit.objects.create(**associated_with, is_pleasant=True)
        healthy_habit_item = Habit.objects.create(**validated_data, associated_with=pleasant_habit)
        return healthy_habit_item

    def update(self, instance, validated_data):
        associated_with_data = validated_data.pop('associated_with')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        for key, value in associated_with_data.items():
            setattr(instance.associated_with, key, value)
        instance.associated_with.save()
        instance.save()
        return instance


class HealthWithPleasantHabitSerializer(ModelSerializer):
    associated_with = PleasantHabitSerializer()

    class Meta:
        model = Habit
        exclude = ('reward',)
