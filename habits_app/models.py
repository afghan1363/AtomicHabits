from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db.models.query_utils import Q

NULLABLE = {'blank': True, 'null': True}


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
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Повторять каждый <номер> день',
                                                   validators=(MinValueValidator(1), MaxValueValidator(7)))
    reward = models.CharField(max_length=500, verbose_name='Вознаграждение', **NULLABLE)
    execution_time = models.PositiveSmallIntegerField(default=120, verbose_name='Время на исполнение привычки, сек',
                                                      validators=(MaxValueValidator(120),))
    is_public = models.BooleanField(default=False, verbose_name='Открыта для всех')

    def __str__(self):
        return f'{self.action} - приятная' if self.is_pleasant else f'{self.action} - полезная'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        constraints = [
            models.CheckConstraint(
                check=
                Q(
                    is_pleasant=True,
                    reward__isnull=True,
                    associated_with__isnull=True
                )
                |
                Q(
                    is_pleasant=False,
                    reward__isnull=True,
                    associated_with__isnull=False

                )
                |
                Q(
                    is_pleasant=False,
                    reward__isnull=False,
                    associated_with__isnull=True
                ),
                name='is_pleasant_or_reward_or_associated'
            )
        ]
