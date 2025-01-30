# product_special_offer/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import SpecialOffer


class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = (
    'product', 'original_price', 'discount_percentage', 'discounted_price', 'offer_period', 'image_thumbnail')
    list_filter = ('offer_start_date', 'offer_end_date')
    search_fields = ('product__name',)
    readonly_fields = ('discounted_price', 'original_price', 'image_thumbnail')

    def discounted_price(self, obj):
        return f"${obj.get_discounted_price():.2f}"

    discounted_price.short_description = 'Discounted Price'

    def original_price(self, obj):
        return f"${obj.product.price:.2f}"

    original_price.short_description = 'Original Price'

    def offer_period(self, obj):
        return f"{obj.offer_start_date.strftime('%Y-%m-%d')} to {obj.offer_end_date.strftime('%Y-%m-%d')}"

    offer_period.short_description = 'Offer Period'

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = 'Image'


# Register the admin class with the model
admin.site.register(SpecialOffer, SpecialOfferAdmin)
