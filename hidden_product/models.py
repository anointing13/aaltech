from django.db import models
from aaltech.product.models import Product


class HiddenProduct(Product):
    class Meta:
        proxy = True  # This makes HiddenProduct a proxy model, inheriting Product's table

    @classmethod
    def get_hidden_products(cls, query=None):
        """Retrieve hidden products based on search query."""
        hidden_products = cls.objects.filter(is_hidden=True)
        if query:
            hidden_products = hidden_products.filter(name__icontains=query)
        return hidden_products
