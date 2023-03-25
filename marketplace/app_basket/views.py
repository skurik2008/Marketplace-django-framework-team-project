#!/usr/bin/env python
# -*- coding: utf8 -*-

from app_merch.models import Offer
from django.shortcuts import render

from .cart import CartService


def get_cart(request):
    """
    View получения корзины товаров юзера на странице сайта
    """
    cart_user = CartService(request)
    return render(request, 'cart.html', context={'cart': cart_user.get_cart_item_list()})

def add_to_cart(request):
    """
    View добавления товара в корзину
    """
    quantity = request.POST.get('amount', 1)
    offer_id = request.POST.get('offer_id')
    offer = Offer.objects.get(id=offer_id)
    cart_user = CartService(request)
    cart_user.add_offer(offer=offer, quantity=quantity)

def remove_from_cart(request):
    """
    View удаления товара из корзины
    """
    offer_id = request.POST.get('offer_id')
    offer = Offer.objects.get(id=offer_id)
    cart_user = CartService(request)
    cart_user.delete_offer(offer)
