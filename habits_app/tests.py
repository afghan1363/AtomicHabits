from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits_app.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.com', password='Test12345')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """
        Create habit with reward
        """
        data = {
            'place': 'place_test',
            'action_time': '2024-02-14 12:30',
            'action': 'action_test',
            'periodicity': 7,
            'reward': 'reward_test',
            'execution_time': 100,
            'is_public': False
        }
        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {'id': response.json()['id'], 'associated_with': None, 'place': 'place_test',
             'action_time': '2024-02-14 12:30',
             'action': 'action_test', 'is_pleasant': False, 'periodicity': 7, 'reward': 'reward_test',
             'execution_time': 100, 'is_public': False, 'user': self.user.pk}
        )
        self.assertTrue(Habit.objects.all().exists())

    def test_create_wrong_habit(self):
        """
        Create wrong habit
        """
        data = {
            'place': 'place_test',
            'action_time': '2024-02-14 12:30',
            'action': 'action_test',
            'is_pleasant': True,
            'reward': 'test_reward',
            'periodicity': 7,
            'execution_time': 100,
            'is_public': False
        }
        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Приятная привычка сама уже как награда:)']}
        )

    def test_create_habit_with_pleasant_habit(self):
        """
        Create health with pleasant habits
        """
        data = {
            "associated_with": {
                "place": "In Cafe UPD2",
                "action": "Drink a orange and green apple fresh",
                "execution_time": 30,
                "is_public": True,
            },
            "place": "In Park UPD2",
            "action_time": "2024-02-01 15:00",
            "action": "Run and fast walk",
            "periodicity": 2,
            "execution_time": 120,
            "is_public": True,
        }
        response = self.client.post(reverse('habits_app:create_habit'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {'id': response.json()['id'],
                          'associated_with': {
                              'id': response.json()['associated_with']['id'], 'is_pleasant': True,
                              'place': 'In Cafe UPD2',
                              'action': 'Drink a orange and green apple fresh',
                              'periodicity': 2, 'execution_time': 30, 'is_public': True,
                              'user': response.json()['user']}, 'place': 'In Park UPD2',
                          'action_time': '2024-02-01 15:00', 'action': 'Run and fast walk', 'is_pleasant': False,
                          'periodicity': 2, 'reward': None, 'execution_time': 120, 'is_public': True,
                          'user': response.json()['user']}

                         )

    def test_create_wrong_associated_habit(self):
        """
        Create habit with wrong pleasant habit
        """
        data = {
            "associated_with": {
                "is_pleasant": False,
                "place": "In Cafe UPD2",
                "action": "Drink a orange and green apple fresh",
                "execution_time": 30,
                "is_public": True,
            },
            "place": "In Park UPD2",
            "action_time": "2024-02-01 15:00",
            "action": "Run and fast walk",
            "periodicity": 2,
            "execution_time": 120,
            "is_public": True,
        }
        response = self.client.post(reverse('habits_app:create_habit'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У полезной привычки может быть связанной только приятная привычка']}
        )

    def test_habits_update(self):
        """
        Test updating habit
        :return:
        """
        data = {
            "associated_with": {
                "place": "In Cafe ",
                "action": "Drink a orange and green apple fresh",
                "execution_time": 30,
                "is_public": True,
            },
            "place": "In Park ",
            "action_time": "2024-02-01 15:00",
            "action": "Run and fast walk",
            "periodicity": 2,
            "execution_time": 120,
            "is_public": True,
        }
        data_upd = {'associated_with': {
            'is_pleasant': True,
            'place': 'In Cafe UPD2',
            'action': 'Drink a orange and green apple fresh',
            'execution_time': 30,
            'is_public': True
        },
            'place': 'In Park UPD2',
            'action_time': '2024-02-01 15:00',
            'action': 'Run and fast walk',
            'is_pleasant': False,
            'periodicity': 2,
            'reward': None,
            'execution_time': 120,
            'is_public': True}

        posted = self.client.post(reverse('habits_app:create_habit'), data, format='json')
        response = self.client.patch(reverse('habits_app:update_habit', kwargs={'pk': posted.json()['id']}),
                                     data_upd, format='json')
        self.assertEqual(response.json(), {'id': posted.json()['id'],
                                           'associated_with': {'id': posted.json()['associated_with']['id'],
                                                               'is_pleasant': True, 'place': 'In Cafe UPD2',
                                                               'action': 'Drink a orange and green apple fresh',
                                                               'periodicity': 2, 'execution_time': 30,
                                                               'is_public': True, 'user': posted.json()['user']},
                                           'place': 'In Park UPD2',
                                           'action_time': '2024-02-01 15:00', 'action': 'Run and fast walk',
                                           'is_pleasant': False, 'periodicity': 2, 'reward': None,
                                           'execution_time': 120, 'is_public': True, 'user': posted.json()['user']}
                         )

    def test_habit_delete(self):
        """
        Test destroying habit
        """
        data = {
            "associated_with": {
                "place": "In Cafe ",
                "action": "Drink a orange and green apple fresh",
                "execution_time": 30,
                "is_public": True,
            },
            "place": "In Park ",
            "action_time": "2024-02-01 15:00",
            "action": "Run and fast walk",
            "periodicity": 2,
            "execution_time": 120,
            "is_public": True,
        }
        posted = self.client.post(reverse('habits_app:create_habit'), data, format='json')
        response = self.client.delete(reverse('habits_app:destroy_habit', kwargs={'pk': posted.json()['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
