from rest_framework.exceptions import ValidationError


class ValidHabit:
    """
    Валидация создания/редактирования привычки
    """

    def __call__(self, value):
        pleasant_habit = dict(value).get('is_pleasant')
        pleasant_habit_associated = dict(value).get('associated_with')
        reward = dict(value).get('reward')
        action_time = dict(value).get('action_time')
        if not action_time:
            if not pleasant_habit or pleasant_habit_associated or reward:
                raise ValidationError('Это приятная привычка, с которой связана полезная привычка')
        elif pleasant_habit_associated and pleasant_habit:
            raise ValidationError('Приятная привычка не может иметь связанную с ней приятную привычку')
        elif reward and pleasant_habit:
            raise ValidationError('Приятная привычка сама уже как награда:)')
        elif ((not pleasant_habit and reward and pleasant_habit_associated) or
              (not pleasant_habit and not reward and not pleasant_habit_associated)):
            raise ValidationError('У полезной привычки может быть либо вознаграждение либо приятная привычка')
        elif pleasant_habit_associated and not pleasant_habit:
            if not dict(pleasant_habit_associated).get('is_pleasant'):
                raise ValidationError('У полезной привычки может быть связанной только приятная привычка')


class ValidPost:
    """
    Исключение использования не входящих в привычку полей
    """
    def __init__(self, fields: tuple):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = dict(value).get(field)
            if field_value:
                raise ValidationError(f'Поле {field} исключено для этой привычки')
