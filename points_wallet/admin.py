from django.contrib import admin
from .models import Wallet, Transaction, Withdrawal


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'last_login_date')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'transaction_type', 'points', 'created_at', 'product_details')

    def product_details(self, obj):
        if obj.product:
            return f"{obj.product.name} - {obj.product_price} USD"
        return "No Product"

    product_details.short_description = 'Product and Price'  # Custom column name in admin


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'full_name', 'mobile_money_number', 'points', 'status', 'created_at')
    actions = ['mark_as_sent']

    def mark_as_sent(self, request, queryset):
        queryset.update(status='SENT')

    mark_as_sent.short_description = "Mark selected withdrawals as sent"
