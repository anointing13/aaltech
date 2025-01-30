# faq/models.py
from django.db import models
from django.conf import settings


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)  # New field to hide/display FAQs

    def __str__(self):
        return self.question

# Create your models here.


