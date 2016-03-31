# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import (
    Category,
    Product,
    Variation,
)


class VariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variation
        fileds = [
            # 'id',
            'title',
            'price',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    variation_set = VariationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='product_detail_api')
    # variation_set = VariationSerializer(many=True, read_only=True)
    variation_set = VariationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'title',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='category_detail_api')
    product_set = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'title',
            'description',
            # obj.product_set.all()
            'product_set',
            # 'default_category',
        ]
