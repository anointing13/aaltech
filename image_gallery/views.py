from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Gallery, GalleryImage
from django.views.generic import DetailView


# View for listing all galleries with pagination
def gallery_list(request):
    galleries = Gallery.objects.all().order_by('-created_at')  # Get all galleries
    paginator = Paginator(galleries, 4)  # Show 4 galleries per page

    page_number = request.GET.get('page')
    gallery_page = paginator.get_page(page_number)

    return render(request, 'image_gallery/gallery_list.html', {'galleries': gallery_page})



# Detail view for a specific gallery, displaying images within that gallery


class GalleryDetailView(DetailView):
    model = Gallery  # Specify the model to use
    template_name = 'image_gallery/gallery_detail.html'  # Template for the detail view
    context_object_name = 'gallery'  # The context variable name for the object

    def get_object(self, queryset=None):
        # Get the gallery object by its slug, not pk
        return get_object_or_404(self.model, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the images for this gallery and add them to the context
        context['images'] = GalleryImage.objects.filter(gallery=self.object)  # All images in this gallery
        return context
