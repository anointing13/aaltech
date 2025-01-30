from django.conf import settings
from django.db import models







class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_destination = models.CharField(max_length=255, default='Unknown', null=False, blank=False)  # Default value if not provided
    to_destination = models.CharField(max_length=255, default='Unknown', null=False, blank=False)     # Default value if not provided
    booking_date = models.DateField(null=False, blank=False)
    # number_of_seat = models.PositiveIntegerField(null=False, blank=False)
    price_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=False, blank=False)
    payment_status = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return f"Booking by {self.user} on {self.booking_date} from {self.from_destination} to {self.to_destination}"




class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LoyaltyPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
