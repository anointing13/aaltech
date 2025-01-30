# news/models.py

from django.db import models
from django.utils.text import slugify


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')  # ImageField for news images
    published_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# New model for news details
class NewsDetail(models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='details')
    full_content = models.TextField()

    def __str__(self):
        return f"Details for {self.news.title}"