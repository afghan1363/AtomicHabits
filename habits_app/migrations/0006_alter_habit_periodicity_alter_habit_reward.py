# Generated by Django 5.0.1 on 2024-02-06 15:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_app', '0005_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='Повторять каждый <номер> день'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='reward',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Вознаграждение'),
        ),
    ]
