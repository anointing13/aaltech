from django.contrib import admin
from .models import Career


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')  # Fields to display in the admin list
    search_fields = ('name', 'email', 'phone_number')  # Fields to search by
    list_filter = ('email',)  # Filters based on the email field
