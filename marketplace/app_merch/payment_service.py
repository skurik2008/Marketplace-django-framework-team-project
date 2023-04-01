import requests

from marketplace.settings import PURCHASE_URL


def pay_for_the_order(
        username: str,
        order_id: int,
        card_number: str,
        amount: float
):
    """
    Функция отправки запроса на оплату заказа.
    В ответе получаем JSON со статусом оплаты.
    """
    response = requests.post(
        url=PURCHASE_URL,
        json={
            "username": username,
            "order_id": order_id,
            "card_number": card_number,
            "amount": amount
        }
    )
    return response.json()
