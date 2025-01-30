# accounts/email_utils.py
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from .utils import get_recipient_emails  # Import the utility function


def send_email():
    # Mailtrap SMTP server details
    SMTP_HOST = 'sandbox.smtp.mailtrap.io'  # Mailtrap SMTP server
    SMTP_PORT = '2525'  # Port number (587 is typical for TLS)
    SMTP_USER = '6a2b0e226b1a21'  # Your Mailtrap username
    SMTP_PASSWORD = 'a47f1803341e2c'  # Your Mailtrap password

    # Get recipient emails from the database
    recipient_emails = get_recipient_emails()

    if not recipient_emails:
        print('No recipient emails found.')
        return

    # Email details
    msg = MIMEText('This is a test email')
    msg['Subject'] = 'Test Email'
    msg['From'] = 'slygee46@gmail.com'
    msg['To'] = ', '.join(recipient_emails)  # Multiple recipients

    # Send email
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print('Email sent successfully')
    except Exception as e:
        print(f'Error: {e}')
