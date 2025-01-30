# newsletter/send_newsletter.py
from django.core.mail import send_mail
from .models import Subscriber


def send_newsletter(subject, message):
    emails = Subscriber.objects.values_list('email', flat=True)
    send_mail(
        subject=subject,
        message=message,
        from_email='your-email@example.com',
        recipient_list=list(emails),
        fail_silently=False,
    )
