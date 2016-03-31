# -*- coding: utf-8 -*-
from django_filters import FilterSet, CharFilter, NumberFilter
from .models import Product


# Seart機能の便利Plugin活用
class ProductFilter(FilterSet):
    title = CharFilter(
        name='title', lookup_type='icontains')
    category = CharFilter(
        name='categories__title', lookup_type='icontains', distinct=True)
    category_id = CharFilter(
        name='categories__id', lookup_type='icontains', distinct=True)

    min_price = NumberFilter(
        name='variation__price', lookup_type='gte', distinct=True)
    max_price = NumberFilter(
        name='variation__price', lookup_type='lte', distinct=True)

    class Meta:
        model = Product
        fileds = [
            'min_price',
            'max_price',
            'category',
            'title',
            'description',
        ]
