import pytest
from unittest import mock

from stock_exchange.use_cases import request_objects as req
from stock_exchange.shared import response_object as res
from stock_exchange.use_cases import order_use_case as ouc


@pytest.fixture
def order_quote():
    return "SNAP BID: 20.00 ASK: 21.00 LAST: 20.00"


def test_order_quote_with_stock_name(order_quote):
    repo = mock.Mock()
    repo.quote.return_value = order_quote

    order_list_use_case = ouc.OrderQuoteUseCase(repo)
    command = {'stock_name': "SNAP"}
    request_object = req.OrderQuoteRequestObject.from_dict({'command': command})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is True

    repo.quote.assert_called_with(stock_name="SNAP")
    assert response_object.value == order_quote


def test_order_quote_handles_generic_error():
    repo = mock.Mock()
    repo.quote.side_effect = Exception("Just an error message")

    order_list_use_case = ouc.OrderQuoteUseCase(repo)
    command = {'stock_name': "SNAP"}
    request_object = req.OrderQuoteRequestObject.from_dict({'command': command})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.SYSTEM_ERROR,
        'message': "Exception: Just an error message"
    }


def test_order_quote_handles_bad_request():
    repo = mock.Mock()

    order_list_use_case = ouc.OrderQuoteUseCase(repo)
    request_object = req.OrderQuoteRequestObject.from_dict({'command': 5})

    response_object = order_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "command: Is not iterable"
    }
