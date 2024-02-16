from rest_framework.serializers import ModelSerializer, IntegerField, BooleanField
from habits_app.models import Habit
from habits_app.validators import ValidPost, ValidHabit


class PleasantHabitSerializer(ModelSerializer):
    """
    Сериализатор приятной привычки
    """
    is_pleasant = BooleanField(default=True)
    periodicity = IntegerField(read_only=True)

    class Meta:
        model = Habit
        exclude = ('action_time', 'reward', 'associated_with',)
        validators = (ValidPost(fields=exclude),)

    def create(self, validated_data):
        pleasant_habit = Habit.objects.create(**validated_data)
        return pleasant_habit


class HabitSerializer(ModelSerializer):
    """
    Сериализатор привычки
    """
    associated_with = PleasantHabitSerializer(allow_null=True, default=None)

    class Meta:
        model = Habit
        fields = '__all__'


class HealthWithPleasantHabitCreateSerializer(ModelSerializer):
    """
    Сериализатор создания и редактирования полезной привычки со связанной с нею приятной привычкой
    """
    associated_with = PleasantHabitSerializer(allow_null=True, default=None)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = (ValidHabit(),)

    def create(self, validated_data):
        associated_with = validated_data.pop('associated_with', None)
        if associated_with:
            pleasant_habit = Habit.objects.create(**associated_with, user=validated_data.get('user'),
                                                  periodicity=validated_data.get('periodicity'))
            healthy_habit_item = Habit.objects.create(**validated_data, associated_with=pleasant_habit)
        else:
            healthy_habit_item = Habit.objects.create(**validated_data)
        return healthy_habit_item

    def update(self, instance, validated_data):
        associated_with_data = validated_data.pop('associated_with', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if associated_with_data:
            for key, value in associated_with_data.items():
                setattr(instance.associated_with, key, value)
            instance.associated_with.save()
        instance.save()
        return instance
