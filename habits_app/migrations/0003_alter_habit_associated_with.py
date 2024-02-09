# Generated by Django 5.0.1 on 2024-01-31 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_app', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='associated_with',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pleasant', to='habits_app.habit', verbose_name='Связанная приятная привычка'),
        ),
    ]