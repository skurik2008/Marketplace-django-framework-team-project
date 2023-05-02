#!/usr/bin/env python
# -*- coding: utf8 -*-
from datetime import datetime

from .models import Product

VIEWED_PRODUCTS = 'viewed_products'
NUMBER_ITEMS_IN_LIST = 20

class ViewedProducts:
    """ Класс-сервис для просмотренных товаров """

    def add_item(self, request, product_id):
        """
        Метод создает список-словарь (id товара: дата просмотра) просмотренных товаров в session,
        добавляет в него новые либо обновляет дату просмотра в старых товарах,
        при этом регулируется общее число товаров в списке согласно переменной NUMBER_ITEMS_IN_LIST
        """

        if VIEWED_PRODUCTS not in request.session:
            request.session[VIEWED_PRODUCTS] = {str(product_id): f"{datetime.now()}"}
        else:
            dict_viewed_products = request.session[VIEWED_PRODUCTS]
            if len(dict_viewed_products) == NUMBER_ITEMS_IN_LIST:
                if str(product_id) not in dict_viewed_products.keys():
                    sorted_id_by_date = sorted(dict_viewed_products, key=dict_viewed_products.get)
                    id_for_delete = sorted_id_by_date[0]
                    del dict_viewed_products[id_for_delete]

            dict_viewed_products.update({str(product_id): f"{datetime.now()}"})
            request.session[VIEWED_PRODUCTS] = dict_viewed_products

    def delete_item(self, request, product_id):
        """ Метод удаляет товар из списка-словаря просмотренных товаров"""
        request.session[VIEWED_PRODUCTS].pop(product_id, None)

    def get_list_viewed_products(self, request):
        """
        Метод получения списка просмотренных товаров, отсортированных по дате просмотра (начиная с раннего)
        """
        dict_viewed_products = request.session[VIEWED_PRODUCTS]
        sorted_product_id = sorted(dict_viewed_products, key=dict_viewed_products.get, reverse=True)
        list_sorted_products = [Product.objects.get(id=id) for id in sorted_product_id]
        return list_sorted_products
