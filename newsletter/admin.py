# newsletter/admin.py
from django.contrib import admin
from .models import Subscriber
import csv
from django.http import HttpResponse


@admin.action(description='Export Selected Subscribers')
def export_subscribers(_modeladmin, _request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed At'])
    for subscriber in queryset:
        writer.writerow([subscriber.email, subscriber.subscribed_at])
    return response


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    actions = [export_subscribers]
