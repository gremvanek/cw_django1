from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            username='admin@sky.pro',
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123qwe456rty')
        user.save()