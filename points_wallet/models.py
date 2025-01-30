from django.db import models
from django.conf import settings

from product.models import Product


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    points = models.PositiveIntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Wallet - {self.points} Points"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('PURCHASE_BONUS', 'Purchase Bonus'),
        ('BIG_PURCHASE_BONUS', 'Big Purchase Bonus'),
        ('LOGIN_BONUS', 'Login Bonus'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('PURCHASE', 'Purchase'),  # Added a new transaction type for purchases
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)  # Link to product
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Store price
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.points} Points - {self.product.name if self.product else 'No Product'}"


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="withdrawals")
    full_name = models.CharField(max_length=100)
    mobile_money_number = models.CharField(max_length=15)
    points = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.email} - {self.status} ({self.points} Points)"
