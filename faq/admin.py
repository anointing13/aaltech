from django.contrib import admin
from .models import FAQ


# Registering the FAQ model
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')  # Fields to display in the admin list view
    search_fields = ('question', 'answer')  # Adds a search bar to the admin interface
    list_filter = ('question',)  # Adds filtering options in the sidebar
