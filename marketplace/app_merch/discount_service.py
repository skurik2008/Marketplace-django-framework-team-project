from decimal import Decimal
from itertools import chain
from typing import List

from app_basket.models import CartItem
from django.db.models import Avg, Count, Max, Q
from django.utils import timezone

from .models import Discount, Offer, Product, SetDiscount, SetOfProducts


class DiscountService:
    def calculate_average_price(self, offers):
        """
        Метод для расчета средней цены на основе списка предложений.
        """

        return offers.aggregate(Avg("price"))["price__avg"]

    def calculate_price_with_discount(self, offer, discount):
        """
        Метод для расчета цены с учетом скидки на основе предложения и скидки.
        """
        offer_price_with_discount = (
            offer.price * (1 - Decimal(discount.size) / 100)
            if discount.is_percent
            else offer.price - discount.size
        )
        return offer_price_with_discount

    def get_offers_with_and_without_discount(self, offers):
        """
        Метод для получения списка предложений со скидками и без скидок на основе списка предложений.
        """
        current_time = timezone.now()
        offers_with_discount, offers_without_discount = [], []
        for offer in offers:
            set_discounts = Discount.objects.filter(
                is_active=True,
                product=None,
                set_of_products__isnull=False,
                start_date__lte=current_time,
                end_date__gte=current_time,
            )
            discounts = Discount.objects.filter(
                product=offer.product,
                is_active=True,
                start_date__lte=current_time,
                end_date__gte=current_time,
            )
            if discounts.exists():
                discount = discounts.first()
                offer_price_with_discount = self.calculate_price_with_discount(
                    offer, discount
                )
                offers_with_discount.append((offer, offer_price_with_discount))
            else:
                offers_without_discount.append((offer, offer.price))
        return offers_with_discount, offers_without_discount

    def calculate_average_with_discount(
        self, offers_with_discount, offers_without_discount
    ):
        """
        Метод для расчета средней цены с учетом скидок на основе списка предложений со скидками и без скидок.
        """
        total_price = 0
        count = 0
        for offer, price_with_discount in offers_with_discount:
            total_price += price_with_discount
            count += 1
        for offer, price in offers_without_discount:
            total_price += price
            count += 1
        return total_price / count if count >= 1 else total_price

    def calculate_price_difference(self, average_price, average_with_discount):
        """
        Метод для расчета разницы в цене между средней ценой и средней ценой с учетом скидок.
        """
        return average_price - average_with_discount

    def calculate_percentage_difference(self, price_difference, average_price):
        """
        Метод для расчета процентной разницы в цене между средней ценой и средней ценой с учетом скидок.
        """
        return (price_difference / average_price) * 100 if average_price != 0 else 0

    def combine_offers_with_discount_and_without_discount(
        self, offers_with_discount, offers_without_discount
    ):
        """
        Метод для объединения списка предложений со скидками и без скидок и их сортировки по цене с учетом скидок.
        """
        # offers_combined = list(chain(offers_with_discount, offers_without_discount))
        offers_combined = offers_with_discount + offers_without_discount
        return sorted(offers_combined, key=lambda x: x[1])

    def apply_set_discounts(self, cart):
        total_price = 0

        # создаем список пар (товар, группа товаров), участвующих в корзине
        products_with_groups = [
            (item.offer.product, item.offer.product.productgroup)
            for item in cart.cart_item.all()
        ]

        # создаем множество из групп товаров в списке
        product_groups_set = set(
            [product_group for product, product_group in products_with_groups]
        )

        # для каждой группы товаров в множестве
        for product_group in product_groups_set:
            # Получаем список групп товаров, участвующих в скидке на набор, кроме текущей группы товаров
            other_groups = (
                SetDiscount.objects.exclude(product_groups=product_group)
                .values_list("product_groups", flat=True)
                .distinct()
            )

            # если других групп товаров нет, то переходим к следующей группе
            if not other_groups:
                continue

            # Далее мы находим пару товаров с самыми дешевыми предложениями из текущей группы товаров и из другой
            # группы товаров
            cheapest_from_current_group = (
                Offer.objects.filter(product__product_groups=product_group)
                .order_by("price")
                .first()
            )
            cheapest_from_other_groups = (
                Offer.objects.filter(product__product_groups__in=other_groups)
                .order_by("price")
                .first()
            )

            # Если хотя бы один из товаров не найден, то переходим к следующей группе товаров
            if not cheapest_from_current_group or not cheapest_from_other_groups:
                continue

            # Вычисляем цену для этой пары товаров без скидки на набор
            total_price_without_set_discount = (
                cheapest_from_current_group.price + cheapest_from_other_groups.price
            )

            # Получаем скидку на набор, связанную с текущей группой товаров
            set_discount = SetDiscount.objects.filter(
                product_groups=product_group
            ).first()

            # Если скидка на набор найдена, то вычисляем цену для этой пары товаров с учетом скидки на набор
            if set_discount:
                discount = set_discount.discount
                total_price_with_set_discount = self.calculate_price_with_discount(
                    cheapest_from_current_group, discount
                ) + self.calculate_price_with_discount(
                    cheapest_from_other_groups, discount
                )
                total_price += min(
                    total_price_with_set_discount, total_price_without_set_discount
                )
            else:
                total_price += total_price_without_set_discount

        # Возвращаем общую цену корзины с учетом всех скидок
        return total_price

    def apply_cart_discount(self, cart):
        """
        Применение скидки на корзину покупок к сумме корзины.

        :param cart: Корзина покупок.
        :return: Общая сумма корзины с учетом скидки на корзину, если она есть, иначе общая сумма корзины без скидки.
        """
        current_time = timezone.now()
        discounts = cart.discounts.filter(
            cart=cart,
            is_active=True,
            start_date__lte=current_time,
            end_date__gt=current_time,
        )
        # Если нет скидок, то возвращаем общую стоимость корзины без учета скидки
        if not discounts:
            return cart.get_total_price()

        # Вычисляем общую стоимость товаров в корзине
        total_price = cart.get_total_price()

        # Получаем общее количество товаров в корзине
        total_quantity = cart.get_total_quantity()

        # Применяем скидки к общей стоимости корзины
        for discount in discounts:
            # Пропускаем скидки, которые не подходят по минимальной сумме заказа или минимальному количеству товаров
            if discount.min_order_sum and total_price < discount.min_order_sum:
                continue

            if discount.min_quantity and total_quantity < discount.min_quantity:
                continue

            # Рассчитываем величину скидки
            if discount.is_percent:
                discount_amount = total_price * (
                    Decimal(discount.discount) / Decimal("100.0")
                )
            else:
                discount_amount = Decimal(discount.discount)

            # Применяем скидку к общей стоимости товаров в корзине
            total_price -= discount_amount

        # Возвращаем общую стоимость корзины с учетом примененных скидок
        return total_price
