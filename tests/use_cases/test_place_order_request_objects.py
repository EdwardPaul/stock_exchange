from stock_exchange.use_cases import request_objects as ro


def test_build_file_buy_mkt_request_object_from_empty_dict():
    req = ro.OrderPlaceMktRequestObject.from_dict({})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_buy_mkt_request_object_from_dict_with_filters():
    req = ro.OrderPlaceMktRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "amount": 10}})

    assert req.command == {"stock_name": "FB",
                           "amount": 10}
    assert bool(req) is True


def test_build_order_buy_mkt_request_object_from_dict_with_invalid_filters():
    req = ro.OrderPlaceMktRequestObject.from_dict({'command': 5})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_buy_mkt_request_object_from_dict_without_stock_name():
    req = ro.OrderPlaceMktRequestObject.from_dict({'command': {"amount": 10}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_buy_lmt_request_object_from_dict_without_amount():
    req = ro.OrderPlaceLmtRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "price": 20.00}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_buy_mkt_request_object_from_dict_without_price():
    req = ro.OrderPlaceLmtRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "amount": -10}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_buy_lmt_request_object_from_dict_with_market_price_type_negative_price():
    req = ro.OrderPlaceLmtRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "price": -20.00,
                                                               "amount": 10}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command: price'
    assert bool(req) is False


def test_build_order_buy_mkt_request_object_from_dict_with_market_price_type():
    req = ro.OrderPlaceMktRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "amount": 10}})

    assert req.command == {"stock_name": "FB",
                           "amount": 10}
    assert bool(req) is True


def test_build_order_buy_lmt_request_object_from_dict_with_limit_price_type_negative_amount():
    req = ro.OrderPlaceLmtRequestObject.from_dict({'command': {"stock_name": "FB",
                                                               "price": 20.00,
                                                               "amount": -10}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command: amount'
    assert bool(req) is False
