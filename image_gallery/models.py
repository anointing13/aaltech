from django.db import models
from django.utils.text import slugify


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')  # Link to the Gallery
    image = models.ImageField(upload_to='gallery_images/')  # ImageField for gallery images
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for each image
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image in {self.gallery.title} - {self.caption if self.caption else 'No Caption'}"
