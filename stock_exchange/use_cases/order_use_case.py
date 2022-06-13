from stock_exchange.shared import response_object as res
from stock_exchange.shared.use_case import UseCase


class OrderViewUseCase(UseCase):
    """Use case performing VIEW ORDERS command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to VIEW ORDERS request object

        Arguments:
            request_object(OrderViewRequestObject): Request object corresponding to VIEW ORDERS

        Returns:
            ResponseSucess: Response handling successful result of the VIEW ORDERS command
        """
        domain_order = self.repo.view()
        return res.ResponseSuccess(domain_order)


class OrderPlaceMktBuyUseCase(UseCase):
    """Use case performing BUY MKT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to BUY MKT request object

        Arguments:
            request_object(OrderPlaceMktRequestObject): Request object corresponding to BUY MKT

        Returns:
            ResponseSucess: Response handling successful result of the BUY MKT command
        """
        order_place = self.repo.place_mkt_buy(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderStopLossBuyUseCase(UseCase):
    """Use case performing BUY MKT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to BUY MKT request object

        Arguments:
            request_object(OrderPlaceMktRequestObject): Request object corresponding to BUY MKT

        Returns:
            ResponseSucess: Response handling successful result of the BUY MKT command
        """
        order_place = self.repo.place_stop_loss_buy(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderStopLossSellUseCase(UseCase):
    """Use case performing BUY MKT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to BUY MKT request object

        Arguments:
            request_object(OrderPlaceMktRequestObject): Request object corresponding to BUY MKT

        Returns:
            ResponseSucess: Response handling successful result of the BUY MKT command
        """
        order_place = self.repo.place_stop_loss_sell(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderPlaceMktSellUseCase(UseCase):
    """Use case performing SELL MKT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to SELL MKT request object

        Arguments:
            request_object(OrderPlaceMktRequestObject): Request object corresponding to SELL MKT

        Returns:
            ResponseSucess: Response handling successful result of the SELL MKT command
        """
        order_place = self.repo.place_mkt_sell(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderPlaceLmtBuyUseCase(UseCase):
    """Use case performing BUY LMT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to BUY LMT request object

        Arguments:
            request_object(OrderPlaceLmtRequestObject): Request object corresponding to BUY LMT

        Returns:
            ResponseSucess: Response handling successful result of the BUY LMT command
        """
        order_place = self.repo.place_lmt_buy(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderPlaceLmtSellUseCase(UseCase):
    """Use case performing SELL LMT command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to SELL LMT request object

        Arguments:
            request_object(OrderPlaceLmtRequestObject): Request object corresponding to SELL LMT

        Returns:
            ResponseSucess: Response handling successful result of the SELL LMT command
        """
        order_place = self.repo.place_lmt_sell(command=request_object.command)
        return res.ResponseSuccess(order_place)


class OrderQuoteUseCase(UseCase):
    """Use case performing QUOTE command

    Arguments:
        repo(MongoRepo): Repository class object to perform database operations
    """
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """Perform database operations corresponding to QUOTE request object

        Arguments:
            request_object(OrderQuoteRequestObject): Request object corresponding to QUOTE

        Returns:
            ResponseSucess: Response handling successful result of the QUOTE command
        """
        order_quote = self.repo.quote(stock_name=request_object.stock_name)
        return res.ResponseSuccess(order_quote)
