from django.db import models


class CheckoutDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    create_account = models.BooleanField(default=False)
    ship_to_different_address = models.BooleanField(default=False)

    # Shipping fields (if 'ship_to_different_address' is True)
    shipping_first_name = models.CharField(max_length=100, blank=True, null=True)
    shipping_last_name = models.CharField(max_length=100, blank=True, null=True)
    shipping_email = models.EmailField(blank=True, null=True)
    shipping_mobile_no = models.CharField(max_length=15, blank=True, null=True)
    shipping_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    shipping_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
