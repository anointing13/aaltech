# accounts/management/commands/test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test sending an email'

    def handle(self, *args, **kwargs):
        try:
            send_mail(
                'Test Subject',
                'This is a test message.',
                settings.DEFAULT_FROM_EMAIL,
                ['slygee46@gmail.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Test email sent successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
