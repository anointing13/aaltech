# Generated by Django 4.2.16 on 2024-10-26 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0003_remove_booking_transport_delete_transport'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='seat_number',
            new_name='number_of_seat',
        ),
    ]
