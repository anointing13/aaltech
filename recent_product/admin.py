# recent_product/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import RecentProduct


class RecentProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name', 'product_code', 'category', 'brand',
        'price', 'units_in_stock', 'image_preview', 'date_added'
    )
    list_filter = ('product__category', 'product__brand', 'date_added')
    search_fields = ('product__name', 'product__code', 'product__category__name', 'product__brand__name')
    readonly_fields = (
        'product_name', 'product_code', 'category', 'brand',
        'price', 'units_in_stock', 'image_preview', 'date_added'
    )
    ordering = ('-date_added',)

    def product_name(self, obj):
        return obj.product.name  # Access product name through the foreign key

    product_name.short_description = 'Product Name'

    def product_code(self, obj):
        return obj.product.code  # Access product code

    product_code.short_description = 'Product Code'

    def category(self, obj):
        return obj.product.category.name if obj.product.category else "No Category"

    category.short_description = 'Category'

    def brand(self, obj):
        return obj.product.brand.name if obj.product.brand else "No Brand"

    brand.short_description = 'Brand'

    def price(self, obj):
        return f"${obj.product.price:.2f}"  # Format price to show as currency

    price.short_description = 'Price'

    def units_in_stock(self, obj):
        return obj.product.units_in_stock  # Display units in stock

    units_in_stock.short_description = 'Units in Stock'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: auto;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


admin.site.register(RecentProduct, RecentProductAdmin)
