from django.db import models


class Career(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    cv = models.FileField(upload_to='cvs/')  # This will store the CV in the 'media/cvs' directory
    cover_letter = models.FileField(upload_to='cover_letters/')  # This will store the Cover Letter in 'media/cover_letters'

    def __str__(self):
        return self.name
