from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}
PERIOD = (
    ('Каждый день', 1),
    ('Через день', 2),
    ('Через два дня', 3),
    ('Через три дня', 4),
    ('Через четыре дня', 5),
    ('Через пять дней', 6),
    ('Раз в неделю', 7),
)


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель привычки',
                             **NULLABLE)
    place = models.CharField(max_length=1000, verbose_name='Место выполнения привычки')
    action_time = models.DateTimeField(verbose_name='Время действия')
    action = models.CharField(max_length=1000, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    associated_with = models.OneToOneField('Habit', on_delete=models.CASCADE,
                                           verbose_name='Связанная приятная привычка', **NULLABLE,
                                           related_name='pleasant')
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность',
                                                   validators=(MinValueValidator(1), MaxValueValidator(7)))
    reward = models.CharField(max_length=500, verbose_name='Вознаграждение')
    execution_time = models.PositiveSmallIntegerField(default=120, verbose_name='Время на исполнение привычки, сек',
                                                      validators=(MaxValueValidator(120),))
    is_public = models.BooleanField(default=False, verbose_name='Открыта для всех')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def clean(self):
        pass
