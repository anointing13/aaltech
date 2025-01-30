"""
URL configuration for aaltech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# from django.views.generic import RedirectView
# from custom_user.views import edit_profile


# from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product.urls')),
    # path('featured/', include('product.urls')),  # or the correct app name
    path('',include('contact.urls')),
    path('accounts/', include('accounts.urls')),
    path('faq/', include('faq.urls')),
    path('checkout/', include('checkout.urls')),
    path('product/', include(('product.urls', 'product'), namespace='product')),  # Include with namespace
    path('payment/', include('payment.urls')),  # Include the payment app's URLs
    path('', include('career.urls')),
    path('oilgas/', include('oilgas.urls')),  # Include oilgas app URLs
    path('', include('transport.urls', namespace='transport')),  # Ensure you use the namespace here
    path('news/', include('news.urls')),  # Include news app URLs
    # path('investor_relations/', include('investor_relations.urls')),  # Include news app URLs
    # path('financial_reports/', include('financial_reports.urls')),
    # path('press_release/', include('press_release.urls')),
    path('image_gallery/', include('image_gallery.urls')),
    path('special-offers/', include('product_special_offer.urls')),
    path('hidden-product/', include('hidden_product.urls')),
    path('recent-product/', include('recent_product.urls')),  # Include the recent_product app
    path('points-wallet/', include('points_wallet.urls', namespace='points_wallet')),  # Include with namespace
    path('', include('help.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('construction/', include('construction.urls')),
    path('events/', include('events.urls')),



    # path('',include('updates.urls')),
    # path("", include("authentication.urls")),
    # path('admin/', RedirectView.as_view(url='/admin'), name="admin"),
    # path('accounts/', include('authentication.urls')),  # Change this line to include authentication URLs
    # path('accounts/', include('custom_user.urls')),
    # path('', include('custom_user.urls')),  # Including custom_user app's URLs
    # path('edit_profile/', edit_profile, name='edit_profile'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
