from stock_exchange.use_cases.request_objects import (
    OrderPlaceLmtRequestObject,
    OrderPlaceMktRequestObject,
    OrderQuoteRequestObject,
    OrderViewRequestObject,
)
from stock_exchange.use_cases.order_use_case import (
    OrderPlaceMktBuyUseCase,
    OrderPlaceMktSellUseCase,
    OrderPlaceLmtBuyUseCase,
    OrderPlaceLmtSellUseCase,
    OrderQuoteUseCase,
    OrderViewUseCase,
)


class ConsoleInterface:
    """Console interface for user interaction

    Attributes:
        repo(:obj:'MongoRepo', optional): Repository class object for interacting with database
        input_list(list): List with user input command
    """
    def __init__(self, repo):
        self.repo = repo
        self.input_list = None

    def run(self):
        """Main loop for user interaction

        Reads user input and performs corresponding actions
        """
        while True:
            self.input_list = self.__get_input()
            if self.input_list[0] == "BUY":
                self.__place_buy_order()
                continue
            if self.input_list[0] == "SELL":
                self.__place_sell_order()
                continue
            if self.input_list[0] == "VIEW":
                self.__place_view_orders()
                continue
            if self.input_list[0] == "QUOTE":
                self.__place_quote()
                continue
            if self.input_list[0] == "QUIT":
                self.repo.db.drop_collection("orders")
                self.repo.db.drop_collection("history")
                break

    def __get_input(self):
        """Processes raw user input from console

        Returns:
            input_list(list): List with user command
        """
        raw_input = input()
        input_list = raw_input.split()
        return input_list

    def __place_buy_mkt_order(self):
        """Performs buy at market price use case"""
        command = {
            "command": {
                "stock_name": self.input_list[1],
                "amount": self.input_list[3]
            }
        }
        request = OrderPlaceMktRequestObject(command)
        place_use_case = OrderPlaceMktBuyUseCase(self.repo)
        result = place_use_case.process_request(request)
        print(result.value)

    def __place_buy_lmt_order(self):
        """Performs buy at user defined price use case"""
        command = {
            "command": {
                "stock_name": self.input_list[1],
                "price": self.input_list[3],
                "amount": self.input_list[4]
            }
        }
        request = OrderPlaceLmtRequestObject(command)
        place_use_case = OrderPlaceLmtBuyUseCase(self.repo)
        result = place_use_case.process_request(request)
        print(result.value)

    def __place_sell_mkt_order(self):
        """Performs sell at market price use case"""
        command = {
            "command": {
                "stock_name": self.input_list[1],
                "amount": self.input_list[3]
            }
        }
        request = OrderPlaceMktRequestObject(command)
        place_use_case = OrderPlaceMktSellUseCase(self.repo)
        result = place_use_case.process_request(request)
        print(result.value)

    def __place_sell_lmt_order(self):
        """Performs sell at user defined price use case"""
        command = {
            "command": {
                "stock_name": self.input_list[1],
                "price": self.input_list[3],
                "amount": self.input_list[4]
            }
        }
        request = OrderPlaceLmtRequestObject(command)
        place_use_case = OrderPlaceLmtSellUseCase(self.repo)
        result = place_use_case.process_request(request)
        print(result.value)

    def __place_view_orders(self):
        """Performs view orders use case"""
        command = {"command": self.input_list[0] + self.input_list[1]}
        request = OrderViewRequestObject(command)
        view_use_case = OrderViewUseCase(self.repo)
        result = view_use_case.process_request(request)
        print(result.value)

    def __place_quote(self):
        """Performs quote use case"""
        command = {"command": {"stock_name": self.input_list[1]}}
        request = OrderQuoteRequestObject.from_dict(command)
        quote_use_case = OrderQuoteUseCase(self.repo)
        result = quote_use_case.process_request(request)
        print(result.value)

    def __place_buy_order(self):
        """Perfroms buy use case"""
        if self.input_list[2] == "MKT":
            self.__place_buy_mkt_order()
        if self.input_list[2] == "LMT":
            self.__place_buy_lmt_order()

    def __place_sell_order(self):
        """Performs sell use case"""
        if self.input_list[2] == "MKT":
            self.__place_sell_mkt_order()
        if self.input_list[2] == "LMT":
            self.__place_sell_lmt_order()
