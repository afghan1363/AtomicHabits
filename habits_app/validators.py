from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


# def valid_associated_habit(value):
#     valid_field = dict(value).get('associated_with')
#     if valid_field:
#         if not dict(valid_field)['is_pleasant']:
#             raise ValidationError('Связанная привычка должна быть приятной')


class ValidPleasantHabit:

    def __call__(self, value):
        pleasant_habit = dict(value).get('is_pleasant')
        pleasant_habit_associated = dict(value).get('associated_with')
        if pleasant_habit_associated and pleasant_habit:
            raise ValidationError('Приятная привычка не может иметь связанную с ней приятную привычку')
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
