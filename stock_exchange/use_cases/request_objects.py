import collections

from stock_exchange.shared.request_objects import (
    ValidRequestObject,
    InvalidRequestObject
)


class OrderPlaceMktRequestObject(ValidRequestObject):
    """Request object corresponding to BUY/SELL MKT command

    Arguments:
        command(dict): Dictionary with BUY/SELL MKT command info
    """
    def __init__(self, command):
        self.command = command

    @classmethod
    def from_dict(cls, input_dict):
        """Generate request from BUY/SELL MKT command dictionary

        Arguments:
            input_dict(dict): BUY/SELL MKT command dictionary with command info

        Returns:
            OrderPlaceMktRequestObject: Valid request object iff command is correct
            InvalidRequestObject: Invalid request iff command is incorrect
        """
        invalid_req = InvalidRequestObject()

        if is_empty(input_dict):
            invalid_req.add_error('command', 'Empty dict')
            return invalid_req

        if is_not_iterable(input_dict):
            invalid_req.add_error('command', 'Is not iterable')
            return invalid_req

        if cls.__is_incomplete(input_dict):
            invalid_req.add_error('command', 'Is incomplete')
            return invalid_req

        if amount_is_negative(input_dict):
            invalid_req.add_error('command: amount', 'Is negative')
            return invalid_req

        return OrderPlaceMktRequestObject(command=input_dict.get('command', None))

    def __is_incomplete(input_dict):
        return not all(k in input_dict['command'] for k in ("stock_name", "amount"))

    def __nonzero__(self):
        return True


class OrderPlaceLmtRequestObject(ValidRequestObject):
    """Request object corresponding to BUY/SELL LMT command

    Arguments:
        command(dict): Dictionary with BUY/SELL LMT command info
    """
    def __init__(self, command):
        self.command = command

    @classmethod
    def from_dict(cls, input_dict):
        """Generate request from BUY/SELL LMT command dictionary

        Arguments:
            input_dict(dict): BUY/SELL LMT command dictionary with command info

        Returns:
            OrderPlaceLmtRequestObject: Valid request object iff command is correct
            InvalidRequestObject: Invalid request iff command is incorrect
        """
        invalid_req = InvalidRequestObject()

        if is_empty(input_dict):
            invalid_req.add_error('command', 'Empty dict')
            return invalid_req

        if is_not_iterable(input_dict):
            invalid_req.add_error('command', 'Is not iterable')
            return invalid_req

        if cls.__is_incomplete(input_dict):
            invalid_req.add_error('command', 'Is incomplete')
            return invalid_req

        if price_is_negative(input_dict):
            invalid_req.add_error('command: price', 'Is negative')
            return invalid_req

        if amount_is_negative(input_dict):
            invalid_req.add_error('command: amount', 'Is negative')
            return invalid_req

        return OrderPlaceLmtRequestObject(command=input_dict.get('command', None))

    def __is_incomplete(input_dict):
        return not all(k in input_dict['command'] for k in ("stock_name",
                                                            "price",
                                                            "amount"))

    def __nonzero__(self):
        return True


class OrderStopLossRequestObject(ValidRequestObject):
    def __init__(self, command):
        self.command = command

    
    @classmethod
    def from_dict(cls, input_dict):
        """Generate request from VIEW ORDERS command dictionary

        Arguments:
            input_dict(dict): VIEW ORDERS command dictionary with command info

        Returns:
            OrderViewRequestObject: Valid request object iff command is correct
            InvalidRequestObject: Invalid request iff command is incorrect
        """
        invalid_req = InvalidRequestObject()

        if cls.__is_empty(input_dict):
            invalid_req.add_error('command', 'Empty dict')
            return invalid_req

        if cls.__is_not_iterable(input_dict):
            invalid_req.add_error('command', 'Is not iterable')
            return invalid_req

        if cls.__is_incomplete(input_dict):
            invalid_req.add_error('command', 'Is incomplete')
            return invalid_req

        if price_is_negative(input_dict):
            invalid_req.add_error('command: price', 'Is negative')
            return invalid_req

        if amount_is_negative(input_dict):
            invalid_req.add_error('command: amount', 'Is negative')
            return invalid_req

        return OrderViewRequestObject(command=input_dict['command'])

    
    def __is_incomplete(input_dict):
        return not all(k in input_dict['command'] for k in ("stock_name",
                                                            "price",
                                                            "amount"))


    def __nonzero__(self):
        return True


class OrderViewRequestObject(ValidRequestObject):
    """Request object corresponding to VIEW ORDERS command

    Arguments:
        command(dict): Dictionary with VIEW ORDERS command info
    """
    def __init__(self, command):
        self.command = command

    @classmethod
    def from_dict(cls, input_dict):
        """Generate request from VIEW ORDERS command dictionary

        Arguments:
            input_dict(dict): VIEW ORDERS command dictionary with command info

        Returns:
            OrderViewRequestObject: Valid request object iff command is correct
            InvalidRequestObject: Invalid request iff command is incorrect
        """
        invalid_req = InvalidRequestObject()

        if cls.__is_empty(input_dict):
            invalid_req.add_error('command', 'Empty dict')
            return invalid_req

        if cls.__is_not_iterable(input_dict):
            invalid_req.add_error('command', 'Is not iterable')
            return invalid_req

        if cls.__wrong_command(input_dict):
            invalid_req.add_error('command', 'Must be VIEW ORDERS')
            return invalid_req

        return OrderViewRequestObject(command=input_dict['command'])

    def __is_empty(input_dict):
        return 'command' not in input_dict.keys()

    def __is_not_iterable(input_dict):
        return ('command' in input_dict.keys()
                and not isinstance(input_dict, collections.Mapping))

    def __wrong_command(input_dict):
        return input_dict['command'] != "VIEW ORDERS"

    def __nonzero__(self):
        return True


class OrderQuoteRequestObject(ValidRequestObject):
    """Request object corresponding to QUOTE command

    Arguments:
        stock_name(str): Name of stock to quote
    """
    def __init__(self, stock_name):
        self.stock_name = stock_name

    @classmethod
    def from_dict(cls, input_dict):
        """Generate request from QUOTE command dictionary

        Arguments:
            input_dict(dict): QUOTE command dictionary with command info

        Returns:
            OrderPlaceLmtRequestObject: Valid request object iff command is correct
            InvalidRequestObject: Invalid request iff command is incorrect
        """
        invalid_req = InvalidRequestObject()

        if is_empty(input_dict):
            invalid_req.add_error('command', 'Empty dict')
            return invalid_req

        if is_not_iterable(input_dict):
            invalid_req.add_error('command', 'Is not iterable')
            return invalid_req

        if cls.__no_stock_name(input_dict):
            invalid_req.add_error('command', 'Stock name not defined')
            return invalid_req

        return OrderQuoteRequestObject(stock_name=input_dict['command']['stock_name'])

    def __no_stock_name(input_dict):
        return "stock_name" not in input_dict['command'].keys()

    def __nonzero__(self):
        return True


def is_empty(input_dict):
    return 'command' not in input_dict


def is_not_iterable(input_dict):
    return ('command' in input_dict
            and not isinstance(input_dict['command'], collections.Mapping))


def amount_is_negative(input_dict):
    return input_dict['command']['amount'] <= 0


def price_is_negative(input_dict):
    return input_dict['command']['price'] <= 0
