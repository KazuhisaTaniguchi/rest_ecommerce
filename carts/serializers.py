# -*- coding: utf-8 -*-
from rest_framework import serializers

from orders.models import UserAddress, UserCheckout
from .models import CartItem, Cart
from .mixins import TokenMixin
from products.models import (
    Variation,
)

"""
{
    "cart_token": "12345",
    "billing_address": 1,
    "shipping_address": 1,
    "checkout_token": "12334"
}

"""


class CheckoutSerializer(TokenMixin, serializers.Serializer):
    checkout_token = serializers.CharField()
    user_checkout_id = serializers.IntegerField(required=False)
    billing_address = serializers.IntegerField()
    shipping_address = serializers.IntegerField()
    cart_token = serializers.CharField()
    cart_id = serializers.IntegerField(required=False)

    def validate(self, data):
        checkout_token = data.get('checkout_token')
        billing_address = data.get('billing_address')
        shipping_address = data.get('shipping_address')
        cart_token = data.get('cart_token')

        checkout_token_data = self.parse_token(checkout_token)
        user_checkout_id = checkout_token_data.get('user_checkout_id')
        print checkout_token_data
        cart_token_data = self.parse_token(cart_token)
        cart_id = cart_token_data.get('cart_id')
        print cart_token_data

        try:
            cart_obj = Cart.objects.get(id=int(cart_id))
            data['cart_id'] = cart_obj.id
        except:
            raise serializers.ValidationError('This is not a valid cart')

        try:
            user_checkout = UserCheckout.objects.get(id=int(user_checkout_id))
            data['user_checkout_id'] = user_checkout.id
        except:
            raise serializers.ValidationError('This is not a valid user')

        try:
            billing_obj = UserAddress.objects.get(
                user__id=int(user_checkout_id), id=int(billing_address))
        except:
            raise serializers.ValidationError(
                'This is not a valid address for this user')
        try:
            shipping_obj = UserAddress.get(
                user__id=int(user_checkout_id), id=int(shipping_address))
        except:
            raise serializers.ValidationError(
                'This is not a valid address for this user')
        return data

    # def validate_<fieldName>(self, value):
    #     some validation here
    #     return value
    # def validate_checkout_token(self, value):
    #     if isinstance(value, str):
    #         return value
    #     raise serializers.ValidationError('This is not a valid token.')


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
