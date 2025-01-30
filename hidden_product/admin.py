from django.contrib import admin
from .models import HiddenProduct


@admin.register(HiddenProduct)
class HiddenProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'units_in_stock', 'is_hidden')
    search_fields = ('name', 'code')
    list_filter = ('is_hidden', 'category', 'brand')

    def get_queryset(self, request):
        # Show only hidden products in this admin view
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=True)
