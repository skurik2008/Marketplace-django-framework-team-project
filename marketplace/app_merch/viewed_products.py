# from datetime import datetime
from django.db.models import QuerySet
from .models import Product, WatchedProduct
from django.utils.timezone import now

# VIEWED_PRODUCTS = 'viewed_products'
# NUMBER_ITEMS_IN_LIST = 20
#
#
# class ViewedProducts:
#     """ Класс-сервис для просмотренных товаров """
#
#     def add_item(self, request, product_id):
#         """
#         Метод создает список-словарь (id товара: дата просмотра) просмотренных товаров в session,
#         добавляет в него новые либо обновляет дату просмотра в старых товарах,
#         при этом регулируется общее число товаров в списке согласно переменной NUMBER_ITEMS_IN_LIST
#         """
#
#         if VIEWED_PRODUCTS not in request.session:
#             request.session[VIEWED_PRODUCTS] = {str(product_id): f"{datetime.now()}"}
#         else:
#             dict_viewed_products = request.session[VIEWED_PRODUCTS]
#             if len(dict_viewed_products) == NUMBER_ITEMS_IN_LIST:
#                 if str(product_id) not in dict_viewed_products.keys():
#                     sorted_id_by_date = sorted(dict_viewed_products, key=dict_viewed_products.get)
#                     id_for_delete = sorted_id_by_date[0]
#                     del dict_viewed_products[id_for_delete]
#
#             dict_viewed_products.update({str(product_id): f"{datetime.now()}"})
#             request.session[VIEWED_PRODUCTS] = dict_viewed_products
#
#     def delete_item(self, request, product_id):
#         """ Метод удаляет товар из списка-словаря просмотренных товаров"""
#         request.session[VIEWED_PRODUCTS].pop(product_id, None)
#
#     def get_list_viewed_products(self, request):
#         """
#         Метод получения списка просмотренных товаров, отсортированных по дате просмотра (начиная с раннего)
#         """
#         dict_viewed_products = request.session[VIEWED_PRODUCTS]
#         sorted_product_id = sorted(dict_viewed_products, key=dict_viewed_products.get, reverse=True)
#         list_sorted_products = [Product.objects.get(id=id) for id in sorted_product_id]
#         return list_sorted_products


class WatchedProductsService:
    products_amount = 20

    def add_product(self, request, product):
        if request.user.is_authenticated:
            watched_products = self.get_watched_products(user=request.user)
            if self.has_product(watched_products=watched_products, product=product):
                watched_product = watched_products.get(product=product)
                watched_product.view_date = now()
                watched_product.save()
            else:
                if self.count_watched_products(watched_products=watched_products) == self.products_amount:
                    self.remove_product(watched_products=watched_products)
                WatchedProduct.objects.create(user=request.user, product=product)
        else:
            if 'watched_products' not in request.session:
                request.session['watched_products'] = {product.id: now()}
            else:
                watched_products = request.session['watched_products']
                if product.id in watched_products.keys():
                    watched_products[product.id] = now()
                else:
                    if len(watched_products) == self.products_amount:
                        watched_products.pop(min(watched_products, key=watched_products.get))
                    watched_products.update({product.id: now()})

    @staticmethod
    def remove_product(watched_products):
        product = watched_products.last()
        product.delete()

    @staticmethod
    def has_product(watched_products, product) -> bool:
        return watched_products.filter(product=product).exists()

    @staticmethod
    def get_watched_products(user, count=None) -> QuerySet:
        queryset = WatchedProduct.objects.filter(user=user).order_by('-view_date')
        if count:
            queryset = queryset[:3]
        return queryset

    @staticmethod
    def count_watched_products(watched_products) -> int:
        return watched_products.count()

    @staticmethod
    def create_watched_products(request):
        for product_id, view_date in request.session['watched_products']:
            product = Product.objects.get(id=product_id)
            WatchedProduct.objects.create(user=request.user, product=product, view_date=view_date)


watched_products_service = WatchedProductsService()
