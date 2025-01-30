from django.contrib import admin
from .models import Order, OrderItem
from django.utils import timezone


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Default to show one empty form for adding new items


# Custom action to mark orders as shipped
def mark_as_shipped(modeladmin, request, queryset):
    queryset.update(status='Shipped', shipped_date=timezone.now())
    modeladmin.message_user(request, "Selected orders have been marked as Shipped.")


mark_as_shipped.short_description = "Mark selected orders as Shipped"


# Custom action to mark orders as delivered
def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status='Delivered')
    modeladmin.message_user(request, "Selected orders have been marked as Delivered.")


mark_as_delivered.short_description = "Mark selected orders as Delivered"


# Custom action to mark orders as cancelled
def mark_as_cancelled(modeladmin, request, queryset):
    queryset.update(status='Cancelled')
    modeladmin.message_user(request, "Selected orders have been marked as Cancelled.")


mark_as_cancelled.short_description = "Mark selected orders as Cancelled"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_number', 'total_amount', 'status', 'shipped_date', 'get_product_names']
    list_filter = ['status', 'shipped_date', 'payment_method']
    search_fields = ['user__email', 'id', 'order_number']
    inlines = [OrderItemInline]
    actions = [mark_as_shipped, mark_as_delivered, mark_as_cancelled]

    def get_product_names(self, obj):
        return ", ".join([str(item.product) for item in obj.items.all()])

    get_product_names.short_description = 'Products'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__user__email', 'product__name']  # Assuming your Product model has a 'name' field
