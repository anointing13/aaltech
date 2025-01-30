from django.contrib import admin
from .models import Appointment, Order
from .models import FuelPrice, FuelPriceHistory


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'date', 'message')  # Display full name in admin
    search_fields = ('customer__email', 'message')  # Allow searching by email or message

    def get_full_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    get_full_name.short_description = 'Full Name'  # Column header in admin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name', 'tonnage', 'super_lpg', 'quantity_of_load', 'station_name', 'car_number', 'driver_name',
        'created_at')  # Display full name in admin
    list_filter = ('tonnage', 'super_lpg')  # Filters for easy management
    search_fields = ('customer__email',)  # Allow searching by email

    def get_full_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    get_full_name.short_description = 'Full Name'  # Column header in admin


class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ('super_price_per_liter', 'lpg_price_per_kilo', 'diesel_price_per_liter', 'updated_at')  # Display diesel price
    list_display_links = ('super_price_per_liter',)  # Make super_price_per_liter clickable
    list_editable = ('lpg_price_per_kilo', 'diesel_price_per_liter')  # Allow lpg and diesel prices to be edited in the list view

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to save a history record when the FuelPrice is updated.
        """
        # First, save the changes to the FuelPrice model
        super().save_model(request, obj, form, change)

        # If the object was changed (prices updated), log the history
        if change:
            FuelPriceHistory.objects.create(
                fuel_price=obj,
                super_price=obj.super_price_per_liter,
                lpg_price=obj.lpg_price_per_kilo,
                diesel_price=obj.diesel_price_per_liter  # Log diesel price as well
            )


# Register the modified admin class
admin.site.register(FuelPrice, FuelPriceAdmin)
