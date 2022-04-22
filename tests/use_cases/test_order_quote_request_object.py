from stock_exchange.use_cases import request_objects as ro


def test_build_file_quote_request_object_from_empty_dict():
    req = ro.OrderQuoteRequestObject.from_dict({})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_quote_request_object_from_dict_with_stock_name():
    req = ro.OrderQuoteRequestObject.from_dict({'command': {"stock_name": "FB"}})

    assert req.stock_name == "FB"
    assert bool(req) is True


def test_build_order_quote_request_object_from_dict_with_invalid_filters():
    req = ro.OrderQuoteRequestObject.from_dict({'command': 5})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_quote_request_object_from_dict_without_stock_name():
    req = ro.OrderQuoteRequestObject.from_dict({'command': {}})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False
