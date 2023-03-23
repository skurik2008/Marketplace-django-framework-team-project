#!/usr/bin/env python
# -*- coding: utf8 -*-

from . import models
from app_users.models import Buyer, Profile


class ItemDoesNotExist(Exception):
    pass

CART_ID = 'cart_id'

class CartService:
    """
    Класс корзины товаров
    """

    def __init__(self, request):
        """
        Инициализируем корзину: ищем уже существующую или создаем ее методом cart_new
        """
        if request.user.is_anonymous:
            cart_id = request.session.get(CART_ID)
            if cart_id:
                cart = models.Cart.objects.filter(id=cart_id).first()
                if cart is None:
                    cart = self.cart_new(request)
            else:
                cart = self.cart_new(request)
        else:
            cart = models.Cart.objects.filter(buyer__profile__user=request.user).first()
            if cart is None:
                cart = self.cart_new(request)

        self.cart = cart

    def cart_new(self, request):
        """
        Создаем корзину (авторизованному пользователю или анониму)
        """
        if request.user.is_anonymous:
            cart = models.Cart.objects.create()
            request.session[CART_ID] = cart.pk
        else:

            cart = models.Cart.objects.create(
                buyer=Buyer.objects.create(profile=Profile.objects.get(user=request.user)))
        return cart

    def add_offer(self, offer, quantity):
        """
        Добавляем товар в корзину
        """
        cart_item = models.CartItem.objects.filter(cart=self.cart, offer=offer).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            models.CartItem.objects.create(offer=offer, cart=self.cart, quantity=quantity)

    def delete_offer(self, offer):
        """
        Удаляем товар из корзины
        """
        cart_item = models.CartItem.object.filter(cart=self.cart, offer=offer).first()
        if cart_item:
            cart_item.delete()
        else:
            raise ItemDoesNotExist

    def change_quantity(self, offer, quantity):
        """
        Меняем количество товара в корзине
        """
        cart_item = models.CartItem.object.filter(cart=self.cart, offer=offer).first()
        if cart_item:
            if quantity == 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
        else:
            raise ItemDoesNotExist

    def get_cart_item_list(self):
        """
        Получаем список товаров в корзине
        """
        return models.CartItem.objects.filter(cart=self.cart)

    def get_cart_item_quantity(self):
        """
        Получаем общее количество товара в корзине
        """
        return models.CartItem.objects.filter(cart=self.cart).count()




