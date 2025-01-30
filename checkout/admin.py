from django.contrib import admin
from .models import CheckoutDetail


@admin.register(CheckoutDetail)
class CheckoutDetailAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_no', 'country', 'city', 'state', 'zip_code')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_no', 'country', 'city', 'state', 'zip_code')
    list_filter = ('country', 'state', 'create_account', 'ship_to_different_address')
