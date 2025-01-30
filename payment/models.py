import random
import string
from django.db import models
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    shipped_date = models.DateTimeField(null=True, blank=True)
    order_number = models.CharField(max_length=8, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_unique_order_number()
        super(Order, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        """Generates a unique 8-digit order number."""
        while True:
            order_number = ''.join(random.choices(string.digits, k=8))
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def __str__(self):
        return f"Order by {self.user.email} - Total: ${self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
