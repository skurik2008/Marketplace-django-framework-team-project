from marketplace.celery import app

from app_merch.payment_service import pay_for_the_order


@app.task
def send_request_to_payment_service(
        username: str,
        order_id: int,
        card_number: str,
        amount: float
):
    """
    Задача, которая будет добавлена в очередь на выполнение.
    Отправляет запрос на оплату заказа.
    """
    response = pay_for_the_order(
        username, order_id, card_number, amount
    )
    return response
