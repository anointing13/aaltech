from django.contrib import admin
from .models import Gallery, GalleryImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Display gallery title and creation date
    search_fields = ('title', 'description')  # Search by title and description
    list_filter = ('created_at',)  # Filter galleries by creation date
    ordering = ('-created_at',)  # Order galleries by creation date (newest first)
    prepopulated_fields = {'slug': ('title',)}  # Auto-populate slug field based on title

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'slug')  # Fields to show in the form
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'image', 'caption', 'uploaded_at')  # Display gallery, image, caption, and upload date
    search_fields = ('caption', 'gallery__title')  # Search by caption and gallery title
    list_filter = ('uploaded_at', 'gallery')  # Filter images by upload date and gallery
    ordering = ('-uploaded_at',)  # Order images by upload date (newest first)

    fieldsets = (
        (None, {
            'fields': ('gallery', 'image', 'caption')  # Fields to show in the form
        }),
    )

