from stock_exchange.domain.order import Order


def test_order_model_init():
    order = Order(
        stock_name="FB",
        price_type="LMT",
        order_type="BUY",
        price=20.00,
        amount="10/20",
    )
    assert order.stock_name == "FB"
    assert order.price_type == "LMT"
    assert order.order_type == "BUY"
    assert order.price == float(20.00)
    assert order.amount == "10/20"


def test_order_model_from_dict():
    order = Order.from_dict(
        {
            'stock_name': "FB",
            'price_type': "LMT",
            'order_type': "BUY",
            'price': 20.00,
            'amount': "10/20",
        }
    )
    assert order.stock_name == "FB"
    assert order.price_type == "LMT"
    assert order.order_type == "BUY"
    assert order.price == float(20.00)
    assert order.amount == "10/20"
