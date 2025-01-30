from django.urls import path
from .views import gallery_list, GalleryDetailView

urlpatterns = [
    path('', gallery_list, name='gallery_list'),  # List of galleries
    path('gallery/<slug:slug>/', GalleryDetailView.as_view(), name='gallery_detail'),  # Detail view for a gallery
]
