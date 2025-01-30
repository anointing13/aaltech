from django.contrib import admin
from .models import Product, Category, Brand


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'discount', 'units_in_stock', 'category', 'brand', 'expiry_date', 'is_hidden')
    list_filter = ('category', 'brand', 'expiry_date', 'is_hidden')
    search_fields = ('name', 'code', 'description')
    list_editable = ('price', 'discount', 'units_in_stock', 'is_hidden')
    fields = ('name', 'code', 'price', 'discount', 'units_in_stock', 'category', 'brand', 'expiry_date', 'image', 'image2',
              'description', 'is_hidden')

    def save_model(self, request, obj, form, change):
        # Custom save logic can be added here
        super().save_model(request, obj, form, change)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)

admin.site.site_header = "My Custom Admin"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Dashboard"
