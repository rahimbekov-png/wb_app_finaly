import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Price больше чем')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Price меньше чем')

    class Meta:
        model = Product
        fields = ['subcategory', 'product_type']