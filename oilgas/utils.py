from .models import FuelPrice
from django.core.exceptions import ObjectDoesNotExist


def get_fuel_price():
    try:
        # Fetch the latest price instance or handle no object case
        return FuelPrice.objects.latest('updated_at')
    except ObjectDoesNotExist:
        return None  # Return None if no price exists
