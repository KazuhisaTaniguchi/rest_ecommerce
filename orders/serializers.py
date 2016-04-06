# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Order, UserAddress


class OrderSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fileds = [
            'id',
            'user',
            'shipping_address',
            'billing_address',
            'shipping_total_price',
            'subtotal',
            'order_total',
        ]

    def get_subtotal(self, obj):
        return obj.cart.sub_total


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fileds = [
            'id',
            'user',
            'type',
            'zipcode',
            'state',
            'address1',
            'address2',
        ]
