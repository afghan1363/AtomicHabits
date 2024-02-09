from django.urls import path
from habits_app.views import *
from habits_app.apps import HabitsAppConfig

app_name = HabitsAppConfig.name

urlpatterns = [
    path('health/reward/create/', HealthHabitWithRewardCreateAPIView.as_view(), name='create_health_reward'),
    path('health/reward/list/', HealthHabitWithRewardListAPIView.as_view(), name='health_rewards'),
    path('health/pleasant/create/', HealthHabitWithPleasantCreateAPIView.as_view(), name='create_health_pleasant'),
    path('health/pleasant/list/', HealthHabitWithPleasantListAPIView.as_view(), name='health_pleasants'),
    path('pleasant/create/', PleasantHabitCreateAPIView.as_view(), name='create_pleasant_habit'),
    path('pleasant/list/', PleasantHabitListAPIView.as_view(), name='pleasant_habits'),
    path('habit/<int:pk>/retrieve/', HabitRetrieveAPIView.as_view(), name='retrieve_habits'),
    path('habit/<int:pk>/destroy/', HabitDestroyAPIView.as_view(), name='destroy_habits'),
]
