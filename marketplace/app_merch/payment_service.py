import requests
from requests.exceptions import ConnectionError, Timeout

from marketplace.settings import PURCHASE_URL


def pay_for_the_order(
        username: str,
        order_id: int,
        card_number: str,
        amount: float
) -> dict | str:
    """
    Функция отправки запроса на оплату заказа.
    В ответе получаем JSON со статусом оплаты.
    """
    try:
        response = requests.post(
            url=PURCHASE_URL,
            json={
                "username": username,
                "order_id": order_id,
                "card_number": card_number,
                "amount": amount
            },
            timeout=10
        )
        return response.json()
    except (ConnectionError, Timeout):
        return "Error: No connection or timeout."
