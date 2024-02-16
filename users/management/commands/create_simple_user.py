from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Создание обычного пользователя
    """
    def handle(self, *args, **options):
        email = input('email: ')
        chat_id = input('chat_id: ')
        first_name = input('first_name: ')
        last_name = input('last_name: ')
        password = 'SkyPro123'
        user = User.objects.create(
            email=email,
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        user.set_password(password)
        user.save()
