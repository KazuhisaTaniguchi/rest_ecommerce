# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import CartItem
from products.models import (
    Variation,
)


class CartVariationSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Variation
        fileds = [
            'id',
            'title',
            'price',
            'product',
        ]

    def get_product(self, obj):
        return obj.product.title


class CartItemSerializer(serializers.ModelSerializer):
    # item = CartVariationSerializer(read_only=True)
    item = serializers.SerializerMethodField()
    item_title = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fileds = [
            'item',
            'item_title',
            'price',
            'product',
            'quantity',
            'line_item_total',
        ]

    def get_item(self, obj):
        return obj.item.id

    def get_item_title(self, obj):
        item_title = obj.item.title
        return item_title

    def get_product(self, obj):
        return obj.item.product.title

    def get_price(self, obj):
        return obj.item.price
