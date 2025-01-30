# accounts/utils.py
from .models import CustomUser


def get_recipient_emails():
    # Query the database for user email addresses
    users = CustomUser.objects.all()  # Adjust query as needed
    emails = [user.email for user in users if user.email]  # Ensure email is not None
    return emails
