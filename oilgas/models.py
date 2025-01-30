from django.conf import settings
from django.db import models


class Appointment(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer} - {self.date}"


class Order(models.Model):
    # Updated tonnage options
    TONNAGE_OPTIONS = [
        ('LPG', 'LPG'),
        ('8-10 tonnes', '8 to 10 Tonnes'),
        ('10-12 tonnes', '10 to 12 Tonnes'),
        ('13-15 tonnes', '13 to 15 Tonnes'),
        ('16-20 tonnes', '16 to 20 Tonnes'),
        ('21-25 tonnes', '21 to 25 Tonnes'),
        ('petrol-diesel', 'Petrol and Diesel'),
        ('9000 litres', '9,000 Litres'),
        ('10000 litres', '10,000 Litres'),
        ('13500 litres', '13,500 Litres'),
        ('15000 litres', '15,000 Litres'),
        ('35000 litres', '35,000 Litres'),
        ('45000 litres', '45,000 Litres'),
    ]

    SUPER_LPG_CHOICES = [
        ('super', 'Super'),  # Correct label for Super
        ('lpg', 'LPG')  # Correct label for LPG
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='oilgas_orders')
    tonnage = models.CharField(max_length=20, choices=TONNAGE_OPTIONS)  # Renamed container_size to tonnage
    super_lpg = models.CharField(max_length=10, choices=SUPER_LPG_CHOICES)  # Renamed oil_or_gas to super_lpg
    quantity_of_load = models.PositiveIntegerField(default=0)  # Default quantity of load set to 0

    # New fields with default values
    tank_capacity = models.CharField(max_length=20, default='10000 litres')  # Default tank capacity
    station_name = models.CharField(max_length=100, default='Main Station')  # Default station name
    car_number = models.CharField(max_length=20, default='Unknown')  # Default car number
    driver_name = models.CharField(max_length=100, default='Not Assigned')  # Default driver name
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow NULL values

    def __str__(self):
        return f"{self.customer} - {self.tonnage} - {self.super_lpg} - {self.quantity_of_load} - {self.car_number} - {self.driver_name}"


class FuelPrice(models.Model):
    super_price_per_liter = models.DecimalField(max_digits=10, decimal_places=2)
    lpg_price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)
    diesel_price_per_liter = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field for diesel price
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Super: {self.super_price_per_liter} per liter, "
            f"LPG: {self.lpg_price_per_kilo} per kilo, "
            f"Diesel: {self.diesel_price_per_liter} per liter"  # Include diesel in the string representation
        )


class FuelPriceHistory(models.Model):
    fuel_price = models.ForeignKey(FuelPrice, on_delete=models.CASCADE)
    super_price = models.DecimalField(max_digits=10, decimal_places=2)
    lpg_price = models.DecimalField(max_digits=10, decimal_places=2)
    diesel_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field for diesel price history
    timestamp = models.DateTimeField(auto_now_add=True)
