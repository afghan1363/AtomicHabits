from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('email: ')
        first_name = input('first_name: ')
        last_name = input('last_name: ')
        password = 'SkyPro123'
        is_moderator = bool(int(input('is_moderator: 1 - True, 0 - False: ')))
        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_moderator=is_moderator
        )
        user.set_password(password)
        user.save()
