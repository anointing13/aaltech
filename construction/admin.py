from django.contrib import admin
from .models import Project
from django.contrib.auth import get_user_model


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'budget', 'manager_name', 'status')
    list_filter = ('is_active',)
    search_fields = ('title', 'first_name', 'last_name')

    # Add custom fields for the manager's first and last name
    def manager_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    manager_name.short_description = 'Manager'

    # Add a method to display the project status (Active/Completed)
    def status(self, obj):
        return "Active" if obj.is_active else "Completed"

    status.short_description = 'Status'

    # Override save_model to save the manager's first and last name
    def save_model(self, request, obj, form, change):
        obj.save()


# Register the model with the admin site
admin.site.register(Project, ProjectAdmin)



