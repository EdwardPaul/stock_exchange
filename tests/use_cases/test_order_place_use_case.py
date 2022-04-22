from unittest import mock

from stock_exchange.use_cases import request_objects as req
from stock_exchange.shared import response_object as res
from stock_exchange.use_cases import order_use_case as ouc


def test_order_mkt_buy_handles_bad_request():
    repo = mock.Mock()

    order_list_use_case = ouc.OrderPlaceMktBuyUseCase(repo)
    request_object = req.OrderPlaceMktRequestObject.from_dict({'command': 5})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "command: Is not iterable"
    }


def test_order_lmt_buy_handles_bad_request():
    repo = mock.Mock()

    order_list_use_case = ouc.OrderPlaceLmtBuyUseCase(repo)
    request_object = req.OrderPlaceLmtRequestObject.from_dict({'command': 5})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "command: Is not iterable"
    }


def test_order_mkt_sell_handles_bad_request():
    repo = mock.Mock()

    order_list_use_case = ouc.OrderPlaceMktSellUseCase(repo)
    request_object = req.OrderPlaceMktRequestObject.from_dict({'command': 5})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "command: Is not iterable"
    }


def test_order_lmt_sell_handles_bad_request():
    repo = mock.Mock()

    order_list_use_case = ouc.OrderPlaceLmtSellUseCase(repo)
    request_object = req.OrderPlaceLmtRequestObject.from_dict({'command': 5})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "command: Is not iterable"
    }
