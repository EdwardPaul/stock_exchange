from stock_exchange.shared.domain_model import DomainModel


class Order(object):
    """Domain entity structure for market order

    Args:
        stock_name(str): Name of stock
        price_type(str): LMT or MKT order price
        order_type(str): BUY or SELL order
        price(float): Price of order
        amount(int): Amount of stocks to buy or sell
    """
    def __init__(self, stock_name, price_type, order_type, price, amount):
        self.stock_name = stock_name
        self.price_type = price_type
        self.order_type = order_type
        self.price = float(price)
        self.amount = amount

    @classmethod
    def from_dict(cls, input_dict):
        """Generate order object from dictionary

        Args:
            input_dict(dict): Input dictionary with order info

        Returns:
            order(Order): Order object made from input dictionary
        """
        order = Order(
            stock_name=input_dict['stock_name'],
            price_type=input_dict['price_type'],
            order_type=input_dict['order_type'],
            price=float(input_dict['price']),
            amount=input_dict['amount'],
        )
        return order

    def to_dict(self):
        """Generate dictionary from Order object

        Returns:
            order_dict(dict): Dictionary with order information
        """
        order_dict = {
            "stock_name": self.stock_name,
            "price_type": self.price_type,
            "order_type": self.order_type,
            "price": self.price,
            "amount": self.amount,
        }
        return order_dict


DomainModel.register(Order)
