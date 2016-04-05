# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from carts.models import Cart


class UserCheckout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.email


ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    zipcode = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    address1 = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return self.state + self.address1

    def get_address(self):
        if self.address2 is None:
            full_address = self.address1
        else:
            full_address = self.address1 + ' ' + self.address2
        return '%s %s %s' % (
            self.zipcode,
            self.state,
            full_address,
        )


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('completed', 'Completed'),
)


class Order(models.Model):
    status = models.CharField(
        max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    billing_address = models.ForeignKey(
        UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(
        UserAddress, related_name='shipping_address', null=True)

    shipping_total_price = models.DecimalField(
        max_digits=20, decimal_places=0, default=10)
    order_total = models.DecimalField(
        max_digits=20, decimal_places=0, default=10)

    def __unicode__(self):
        return str(self.cart.id)

    def mark_completed(self):
        self.status = 'completed'
        self.save()

    def is_complete(self):
        if self.status == 'paid':
            return True
        return False


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)
