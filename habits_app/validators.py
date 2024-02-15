from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from habits_app.models import Habit


# def valid_associated_habit(value):
#     valid_field = dict(value).get('associated_with')
#     if valid_field:
#         if not dict(valid_field)['is_pleasant']:
#             raise ValidationError('Связанная привычка должна быть приятной')


class ValidHabit:

    def __call__(self, value):
        pleasant_habit = dict(value).get('is_pleasant')
        pleasant_habit_associated = dict(value).get('associated_with')
        reward = dict(value).get('reward')
        # id_value = dict(value).get('id')
        # print(value)
        # related_habit = Habit.objects.filter(associated_with_id=id_value)
        # if related_habit:
        #     if not pleasant_habit or pleasant_habit_associated or reward:
        #         raise ValidationError('Это приятная привычка, с которой связана полезная привычка')
        if pleasant_habit_associated and pleasant_habit:
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
    def __init__(self, fields: tuple):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = dict(value).get(field)
            if field_value:
                raise ValidationError(f'Поле {field} исключено для этой привычки')
