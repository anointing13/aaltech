from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal
from django.apps import apps


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # Product fields (unchanged)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=255, unique=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    units_in_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    image2 = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    expiry_date = models.DateField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=10000)
    is_hidden = models.BooleanField(default=False)

    def get_display_price(self):
        # Dynamically load the SpecialOffer model
        SpecialOffer = apps.get_model('product_special_offer', 'SpecialOffer')

        # Attempt to retrieve an active special offer
        active_offer = SpecialOffer.objects.filter(
            product=self,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        # Check if the active offer has expected fields
        if active_offer:
            # Apply discount if it exists, otherwise use special offer price
            if hasattr(active_offer, 'discount') and active_offer.discount:
                return self.price * Decimal((100 - active_offer.discount) / 100)
            elif hasattr(active_offer, 'special_offer_price') and active_offer.special_offer_price:
                return active_offer.special_offer_price

        # Apply product's own discount if no active offer
        if self.discount:
            return self.price * Decimal((100 - self.discount) / 100)

        # Default to original price if no discounts or offers
        return self.price

    def clean(self):
        # Ensure expiry_date is in the future
        if self.expiry_date and self.expiry_date <= timezone.now().date():
            raise ValidationError('Expiry date must be in the future.')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


# Adding Cart and CartItem models for the Add to Cart functionality

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart of {self.user.email}"


# models.py in your cart app

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items', null=True,
                             blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product',
                                on_delete=models.CASCADE)  # Avoid circular import with string reference
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        # Lazy import to avoid circular import issue
        from product_special_offer.models import SpecialOffer

        # Check for active special offers for the product
        active_offer = SpecialOffer.objects.filter(
            product=self.product,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        # If an active special offer exists, use the discounted price
        if active_offer:
            discount_price = self.product.price - (self.product.price * active_offer.discount_percentage / 100)
        else:
            discount_price = self.product.price

        # Calculate the total price considering the quantity and applicable discount
        return self.quantity * discount_price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.get_display_price()  # Use the method to grab the correct price (with or without discount)
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',
                                on_delete=models.CASCADE)  # Using string reference to avoid circular import
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def get_favorite_price(self):
        """Get the price of the product, considering any discounts or special offers."""
        # Dynamically load the SpecialOffer model using apps.get_model() to avoid circular imports
        SpecialOffer = apps.get_model('product_special_offer', 'SpecialOffer')

        # Check if there is an active special offer for the product
        special_offer = SpecialOffer.objects.filter(
            product=self.product,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        # If there is an active special offer, return the discounted price
        if special_offer:
            discount_amount = (self.product.price * special_offer.discount_percentage) / 100
            return self.product.price - discount_amount

        # Return the regular price if there is no special offer
        return self.product.price

    def __str__(self):
        return f"{self.user}'s favorite: {self.product.name}"
