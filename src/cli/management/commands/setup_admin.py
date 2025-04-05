from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from decouple import config

class Command(BaseCommand):
    help = 'Creates an admin user non-interactively if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        SU_NAME = config('DJANGO_SUPERUSER_USERNAME', default=None, cast=str)
        SU_EMAIL = config('DJANGO_SUPERUSER_EMAIL', default=None, cast=str)
        SU_PASSWORD = config('DJANGO_SUPERUSER_PASSWORD', default=None, cast=str)

        if not all([SU_NAME, SU_EMAIL, SU_PASSWORD]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables: DJANGO_SUPERUSER_USERNAME, '
                'DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD'
            ))
            return

        if not User.objects.filter(username=SU_NAME).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser: {SU_NAME}'))
            User.objects.create_superuser(username=SU_NAME, email=SU_EMAIL, password=SU_PASSWORD)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {SU_NAME} already exists. Skipping.'))