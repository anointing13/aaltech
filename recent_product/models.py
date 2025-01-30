# recent_product/models.py
from django.db import models


class RecentProduct(models.Model):
    # Use a string reference for the Product model to avoid circular import issues
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="recent_product")
    image = models.ImageField(upload_to='special_offer_images/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recent Product - {self.product.name}"

    class Meta:
        ordering = ['-date_added']  # Optional: Order by date_added in descending order
