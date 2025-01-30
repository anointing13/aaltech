from django.conf import settings  # Import settings to reference the custom user model
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)  # Directly adding the first name
    last_name = models.CharField(max_length=30, null=True, blank=True)  # Directly adding the last name
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



