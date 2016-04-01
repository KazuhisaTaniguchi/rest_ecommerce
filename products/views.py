# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect, get_object_or_404, render
# from django.utils import timezone

from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import (
    SessionAuthentication,
)
from rest_framework.permissions import (
    IsAuthenticated,
    # IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .filters import ProductFilter

from .pagination import CategoryPagination
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
)

from .forms import VariationInventoryFormSet, ProductFilterForm
from .mixins import StaffRequireMixin
from .models import Product, Variation, Category


import random


# API CBVs
class APIHomeView(APIView):
    def get(self, request, format=None):
        data = {
            'products': {
                'count': Product.objects.all().count(),
                'url': api_reverse('products_api', request=request),
            },
            'categories': {
                'count': Category.objects.all().count(),
                'url': api_reverse('categories_api', request=request),
            },
        }
        return Response(data)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        filters.DjangoFilterBackend,
    ]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    filter_class = ProductFilter


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailUpdateSerializer


# CBVs

class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'products/product_list.html'


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(
            CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products).distinct()
        context['products'] = products
        return context


class VariationListView(StaffRequireMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(
            VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = VariationInventoryFormSet(
            queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):

        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                product_pk = self.kwargs.get('pk')
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()

            messages.success(
                request, 'Your inventory and pricing has been updated.')
            return redirect('products:products')
        raise Http404


def product_list(request):
    qs = Product.objects.all()
    ordering = request.GET.get('ordering')
    if ordering:
        qs = Product.objects.all().order_by(ordering)
    f = ProductFilter(request.GET, queryset=qs)
    context = {
        'object_list': f,
    }
    return render(request, 'products/product_list.html', context)


class FilterMixin(object):
    filter_class = None
    search_ordering_param = 'ordering'

    def get_queryset(self, *args, **kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
        except:
            ImproperlyConfigured(
                'You must have a queryset in order to use the FilterMixin')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            context['object_list'] = f
        return context


class ProductListView(FilterMixin, ListView):
    model = Product
    filter_class = ProductFilter

    def get_context_data(self, *args, **kwargs):
        context = super(
            ProductListView, self).get_context_data(*args, **kwargs)
        # context["now"] = timezone.now()
        context['query'] = self.request.GET.get('q')
        context['filter_form'] = ProductFilterForm(
            data=self.request.GET or None)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(
            ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        context['related'] = sorted(Product.objects.get_related(
            instance)[:6], key=lambda x: random.random())
        return context

# def product_detail_view_func(request, id):
#     product_instance = get_object_or_404(Product, id=id)
#     template = 'products/product_detail.html'
#     context = {
#         'object': product_instance,
#     }
#     return render(request, template, context)
