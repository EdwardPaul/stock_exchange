from stock_exchange.use_cases import request_objects as ro


def test_build_file_view_request_object_from_empty_dict():
    req = ro.OrderViewRequestObject.from_dict({})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_view_request_object_from_dict():
    req = ro.OrderViewRequestObject.from_dict({'command': "VIEW ORDERS"})

    assert req.command == "VIEW ORDERS"
    assert bool(req) is True


def test_build_order_view_request_object_from_dict_with_invalid_command():
    req = ro.OrderViewRequestObject.from_dict({'command': 5})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False


def test_build_order_view_request_object_from_dict_with_wrong_command():
    req = ro.OrderViewRequestObject.from_dict({'command': "VIEWWWWW"})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'command'
    assert bool(req) is False
