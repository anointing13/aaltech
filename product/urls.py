from django.urls import path
from .views import *
from .views import filter_view
from . import views
from .views import favorite_count
from .views import payment_view
from .views import add_to_cart

urlpatterns = [
    path('show/<int:id>/', show, name='show'),
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('shop/show/<int:id>/', show, name='show'),
    # path('checkout/', checkout, name='checkout'),
    path('about/', about, name='about'),
    path('filter/', filter_view, name='filter'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.cart_update_quantity, name='cart_update_quantity'),
    path('cart/remove/<int:item_id>/', views.cart_remove_item, name='cart_remove_item'),
    path('favorites/add/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/', favorites_view, name='favorites_view'),
    path('favorites/remove/<int:product_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/list/', favorites_list, name='favorites_list'),
    path('favorites/count/', favorite_count, name='favorite_count'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('shop/show/<int:id>/', views.show, name='show'),
    path('sammury/', payment_view, name='sammury'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('products-data/', views.products_data, name='products_data'),

]
