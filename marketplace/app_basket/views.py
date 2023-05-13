#!/usr/bin/env python
# -*- coding: utf8 -*-

from app_merch.models import Offer
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .cart import CartService


def get_cart(request):
    """
    View получения корзины товаров юзера на странице сайта
    """
    cart_user = CartService(request)
    return render(
        request, "cart.html", context={"cart_user": cart_user.get_cart_item_list()}
    )


def add_to_cart(request):
    """
    View добавления товара в корзину
    """
    quantity = request.GET.get("amount", 1)
    offer_id = request.GET.get("offer_id")
    offer = Offer.objects.get(id=offer_id)
    cart_user = CartService(request)
    cart_user.add_offer(offer=offer, quantity=quantity)
    return HttpResponseRedirect(redirect_to=request.META.get("HTTP_REFERER"))


def remove_from_cart(request):
    """
    View удаления товара из корзины
    """
    cartitem_id_delete = request.GET.get("cartitem_id")
    CartService(request).delete_cartitem(cartitem_id=cartitem_id_delete)
    return HttpResponseRedirect(redirect_to=request.META.get("HTTP_REFERER"))
