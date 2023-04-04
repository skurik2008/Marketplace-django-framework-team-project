#!/usr/bin/env python
# -*- coding: utf8 -*-
from .cart import CartService

def cart(request):
    """Контекст-процессор, инициализирующий сервис корзины товаров и делающий доступным его всем шаблонам"""
    if request.user.is_superuser:
        return {'cart': []}
    else:
        return {'cart': CartService(request)}