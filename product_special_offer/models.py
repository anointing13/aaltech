# product_special_offer/models.py
from django.db import models
from django.utils import timezone


class SpecialOffer(models.Model):
    # Use a string reference for the Product model to avoid circular import issues
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="special_offers")
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    offer_start_date = models.DateTimeField(default=timezone.now)
    offer_end_date = models.DateTimeField()
    image = models.ImageField(upload_to='special_offer_images/', null=True, blank=True)

    def get_discounted_price(self):
        """Calculate and return the discounted price."""
        discount_amount = (self.product.price * self.discount_percentage) / 100
        return self.product.price - discount_amount

    def is_active(self):
        """Check if the special offer is currently active."""
        now = timezone.now()
        return self.offer_start_date <= now <= self.offer_end_date

    def __str__(self):
        return f"{self.product.name} - {self.discount_percentage}% off"
