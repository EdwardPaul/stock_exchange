import pymongo


class MongoRepo:
    """Repository class for performing operations with MongoDB"""
    def __init__(self):
        # MongoDB client to perform database operations in python
        client = pymongo.MongoClient()
        # MongoDB database
        self.db = client['orders_database']
        # Collection of orders
        self.collection = self.db.orders
        # History of transactions
        self.history = self.db.history

    def view(self):
        """View all orders during client session

        Returns:
            result_string(str): All orders
        """
        orders = self.collection.find()
        result_string = self.__get_result(orders)
        return result_string

    def quote(self, stock_name):
        """Get bid price, ask price and price of last transaction for particular stock

        Arguments:
            stock_name(str): Name of stock for which we want to see info

        Returns:
            str: Bid price, ask price and price of last transaction for particular stock
        """
        bid_price, ask_price, last_price = self.__get_quote_prices(stock_name)
        return "{} BID: {} ASK: {} LAST: {}".format(stock_name, bid_price, ask_price, last_price)

    def place_mkt_buy(self, command):
        """Place buy at market price order

        Arguments:
            command(dict): Dictionary with BUY MKT info
        Returns:
            str: Resulting user output
        """
        order = self.__create_buy_mkt_order(command)
        self.__update_db_mkt_buy(order)
        return "You have placed a MKT {} order for {} {} shares".format(
            order['order_type'],
            order['amount'],
            order['stock_name']
        )

    def place_mkt_sell(self, command):
        """Place sell at market price order

        Arguments:
            command(dict): Dictionary with SELL MKT info
        Returns:
            str: Resulting user output
        """
        order = self.__create_sell_mkt_order(command)
        self.__update_db_mkt_sell(order)
        return "You have placed a MKT {} order for {} {} shares".format(
            order['order_type'],
            order['amount'],
            order['stock_name']
        )

    def place_lmt_buy(self, command):
        """Place buy at user defined price order

        Arguments:
            command(dict): Dictionary with BUY LMT info
        Returns:
            str: Resulting user output
        """
        order = self.__create_buy_lmt_order(command)
        self.__update_db_lmt_buy(order)
        return "You have placed a LMT {} order for {} {} shares at {} each".format(
            order['order_type'],
            order['amount'],
            order['stock_name'],
            order['price']
        )

    
    def place_stop_loss_buy(self, command):
        order = self.__create_stop_loss_buy_order(command)
        self.__update_db_stop_loss_buy(order)
        return "You have placed a STOPLOSS BUY order for {} {} shares at {} each".format(
            order['amount'],
            order['stock_name'],
            order['price'],
        )


    def place_stop_loss_sell(self, command):
        order = self.__create_stop_loss_sell_order(command)
        self.__update_db_stop_loss_sell(order)
        return "You have placed a STOPLOSS SELL order for {} {} shares at {} each".format(
            order['amount'],
            order['stock_name'],
            order['price'],
        )


    def place_lmt_sell(self, command):
        """Place sell at user defined price order

        Arguments:
            command(dict): Dictionary with SELL LMT info
        Returns:
            str: Resulting user output
        """
        order = self.__create_sell_lmt_order(command)
        self.__update_db_lmt_sell(order)
        return "You have placed a LMT {} order for {} {} shares at {} each".format(
            order['order_type'],
            order['amount'],
            order['stock_name'],
            order['price']
        )

    def __get_result(self, orders):
        """Resulting string for VIEW ORDERS command

        Arguments:
            orders(dict): Orders that belong to order DB collection

        Returns:
            str: Resulting string with all orders
        """
        i = 1
        result_string = ""
        for order in orders:
            result_string += "{}. {} {} {} {} {} {}\n".format(i,
                                                              order["stock_name"],
                                                              order["price_type"],
                                                              order["order_type"],
                                                              order["price"],
                                                              order["amount"],
                                                              order["status"])
            i += 1
        return result_string

    def __create_buy_mkt_order(self, command):
        """Create BUY MKT dictionary from command

        Arguments:
            command(dict): Dictionary with command info
        Returns:
            order(dict): Enriched dictionary with command info
        """
        order = command['command']
        order['order_type'] = 'BUY'
        order['price_type'] = 'MKT'
        order['price'] = -1
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order

    
    def __create_stop_loss_buy_order(self, command):
        order = command['command']
        order['order_type'] = "BUY"
        order["price_type"] = "STOPLOSS"
        order['price'] = float(order['price'][1:])
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order

    
    def __create_stop_loss_sell_order(self, command):
        order = command['command']
        order['order_type'] = "SELL"
        order["price_type"] = "STOPLOSS"
        order['price'] = float(order['price'][1:])
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order


    def __create_sell_mkt_order(self, command):
        """Create SELL MKT dictionary from command

        Arguments:
            command(dict): Dictionary with command info
        Returns:
            order(dict): Enriched dictionary with command info
        """
        order = command['command']
        order['order_type'] = 'SELL'
        order['price_type'] = 'MKT'
        order['price'] = -1
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order

    def __create_buy_lmt_order(self, command):
        """Create BUY LMT dictionary from command

        Arguments:
            command(dict): Dictionary with command info
        Returns:
            order(dict): Enriched dictionary with command info
        """
        order = command['command']
        order['order_type'] = 'BUY'
        order['price_type'] = 'LMT'
        order['price'] = float(order['price'].split('$')[-1])
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order

    def __create_sell_lmt_order(self, command):
        """Create SELL LMT dictionary from command

        Arguments:
            command(dict): Dictionary with command info
        Returns:
            order(dict): Enriched dictionary with command info
        """
        order = command['command']
        order['order_type'] = 'SELL'
        order['price_type'] = 'LMT'
        order['price'] = float(order['price'].split('$')[-1])
        order['status'] = 'PENDING'
        order['amount'] = "0/{}".format(order['amount'])
        return order

    def __has_active_sell_orders(self, order):
        return self.collection.count_documents({'stock_name': order['stock_name'],
                                                'order_type': "SELL",
                                                'status': {'$in': ["PENDING", "PARTIAL"]}}) > 0

    def __get_curr_order(self):
        curr_order = self.collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
        curr_order_id = curr_order['_id']
        curr_amount_buy = int(curr_order['amount'].split('/')[0])
        return curr_order, curr_order_id, curr_amount_buy

    def __update_db_mkt_buy(self, order):
        """Perform database operations corresponding to BUY MKT command

        Arguments:
            order(dict): Dictionary with order info
        """
        self.collection.insert_one(order)
        curr_order, curr_order_id, curr_amount_buy = self.__get_curr_order()
        if self.__has_active_sell_orders(order):
            amount_buy = int(order['amount'].split('/')[-1])
            possible_transaction = self.collection.find_one({
                "stock_name": order["stock_name"],
                "order_type": "SELL",
                "status": {'$in': ["PENDING", "PARTIAL"]},
                "price": {'$gt': 0}
            })
            while possible_transaction is not None and amount_buy > 0:
                total_sell_amount = int(possible_transaction['amount'].split('/')[-1])
                curr_sell_amount = int(possible_transaction['amount'].split('/')[0])
                residual = total_sell_amount - curr_sell_amount
                amount_bought = min(amount_buy, residual)
                curr_amount_buy += amount_bought
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "PARTIAL",
                            "amount": "{}/{}".format(curr_amount_buy, amount_buy),
                            "price": float(possible_transaction["price"])
                        }
                    }
                )
                if amount_bought == residual:
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "FILLED",
                                "amount": "{}/{}".format(total_sell_amount, total_sell_amount)
                            }
                        }
                    )
                else:
                    after_transaction_amount = curr_sell_amount + amount_bought
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "PARTIAL",
                                "amount": "{}/{}".format(after_transaction_amount,
                                                         total_sell_amount)
                            }
                        }
                    )
                self.history.insert_one({
                    "stock_name": order["stock_name"],
                    "price": float(possible_transaction['price'])
                })
                self.collection.update_many(
                    {
                        "stock_name": order['stock_name'],
                        "order_type": "SELL",
                        "price": -1
                    },
                    {
                        "$set": {
                            "price": float(possible_transaction['price'])
                        }
                    }
                )
                amount_buy -= amount_bought
                last_price = possible_transaction["price"]
                self.__update_stop_loss(order['stock_name'], last_price)
                possible_transaction = self.collection.find_one(
                    {
                        "stock_name": order["stock_name"],
                        "order_type": "SELL",
                        "status": {
                            '$in': ["PENDING", "PARTIAL"]
                        },
                        "price": {
                            '$gt': 0
                        }
                    }
                )
            if amount_buy == 0:
                total_amount_buy = curr_order['amount'].split('/')[-1]
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "FILLED",
                            "amount": "{}/{}".format(total_amount_buy,
                                                     total_amount_buy),
                            "price": float(last_price)
                        }
                    }
                )


    def __update_stop_loss(self, stock_name, price):
        stop_losses_buy = self.collection.find(
            {
                "stock_name": stock_name,
                "order_type": "BUY",
                "price_type": {
                    '$in': ["STOPLOSS"]
                },
                "price": {
                    '$gte': price
                }
            }
        )
        stop_losses_sell = self.collection.find(
            {
                "stock_name": stock_name,
                "order_type": "SELL",
                "price_type": {
                    '$in': ["STOPLOSS"]
                },
                "price": {
                    '$lte': price
                }
            }
        )
        for order in stop_losses_sell:
            self.collection.update_one(
                    {
                        "_id": order['_id']
                    },
                    {
                        "$set": {
                            "price_type": "LMT",
                        }
                    }
            )
        for order in stop_losses_buy:
            self.collection.update_one(
                    {
                        "_id": order['_id']
                    },
                    {
                        "$set": {
                            "price_type": "LMT",
                        }
                    }
            )



    def __update_db_stop_loss_buy(self, order):
        self.collection.insert_one(order)

    def __update_db_stop_loss_sell(self, order):
        self.collection.insert_one(order)

    def __has_active_buy_orders(self, order):
        return self.collection.count_documents({'stock_name': order['stock_name'],
                                                'order_type': "BUY",
                                                'status': {'$in': ["PENDING", "PARTIAL"]}}) > 0

    def __update_db_mkt_sell(self, order):
        """Perform database operations corresponding to SELL MKT command

        Arguments:
            order(dict): Dictionary with order info
        """
        self.collection.insert_one(order)
        curr_order, curr_order_id, curr_amount_sell = self.__get_curr_order()
        if self.__has_active_buy_orders(order):
            amount_sell = int(order['amount'].split('/')[-1])
            possible_transaction = self.collection.find_one(
                {
                    "stock_name": order["stock_name"],
                    "order_type": "BUY",
                    "status": {
                        '$in': ["PENDING", "PARTIAL"]
                    },
                    "price": {
                        '$gt': 0
                    }
                }
            )
            while possible_transaction is not None and amount_sell > 0:
                total_buy_amount = int(possible_transaction['amount'].split('/')[-1])
                curr_buy_amount = int(possible_transaction['amount'].split('/')[0])
                residual = total_buy_amount - curr_buy_amount
                amount_bought = min(amount_sell, residual)
                curr_amount_sell += amount_bought
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "PARTIAL",
                            "amount": "{}/{}".format(curr_amount_sell, amount_sell),
                            "price": float(possible_transaction["price"])
                        }
                    }
                )
                if amount_bought == residual:
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "FILLED",
                                "amount": "{}/{}".format(total_buy_amount, total_buy_amount)
                            }
                        }
                    )
                else:
                    total_sell_amount = curr_buy_amount + amount_bought
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "PARTIAL",
                                "amount": "{}/{}".format(total_sell_amount, total_buy_amount)}})
                self.history.insert_one({
                    "stock_name": order["stock_name"],
                    "price": float(possible_transaction['price'])
                })
                self.collection.update_many(
                    {
                        "stock_name": order['stock_name'],
                        "order_type": "BUY",
                        "price": -1
                    },
                    {
                        "$set": {
                            "price": float(possible_transaction['price'])
                        }
                    }
                )
                amount_sell -= amount_bought
                last_price = possible_transaction["price"]
                self.__update_stop_loss(order['stock_name'], last_price)
                possible_transaction = self.collection.find_one(
                    {
                        "stock_name": order["stock_name"],
                        "order_type": "BUY",
                        "status": {
                            '$in': ["PENDING", "PARTIAL"]
                        },
                        "price": {
                            '$gt': 0
                        }
                    }
                )
            if amount_sell == 0:
                total_amount = curr_order['amount'].split('/')[-1]
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "FILLED",
                            "amount": "{}/{}".format(total_amount, total_amount),
                            "price": float(last_price)
                        }
                    }
                )

    def __update_db_lmt_buy(self, order):
        """Perform database operations corresponding to BUY LMT command

        Arguments:
            order(dict): Dictionary with order info
        """
        self.collection.insert_one(order)
        curr_order, curr_order_id, curr_amount_buy = self.__get_curr_order()
        if self.__has_active_sell_orders(order):
            amount_buy = int(order['amount'].split('/')[-1])
            possible_transaction = self.collection.find_one(
                {
                    "stock_name": order["stock_name"],
                    "order_type": "SELL",
                    "status": {
                        '$in': ["PENDING", "PARTIAL"]
                    },
                    "$or": [
                        {
                            "price": {
                                '$lte': float(order["price"])
                            }
                        },
                        {
                            "price": {
                                '$eq': -1
                            }
                        }
                    ]
                }
            )
            while possible_transaction is not None and amount_buy > 0:
                total_sell_amount = int(possible_transaction['amount'].split('/')[-1])
                curr_sell_amount = int(possible_transaction['amount'].split('/')[0])
                residual = total_sell_amount - curr_sell_amount
                amount_bought = min(amount_buy, residual)
                curr_amount_buy += amount_bought
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "PARTIAL",
                            "amount": "{}/{}".format(curr_amount_buy,
                                                     amount_buy),
                            "price": order["price"]
                        }
                    }
                )
                if amount_bought == residual:
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "FILLED",
                                "amount": "{}/{}".format(total_sell_amount,
                                                         total_sell_amount)
                            }
                        }
                    )
                else:
                    if possible_transaction["price_type"] == "LMT":
                        sell_amount = curr_sell_amount + amount_bought
                        self.collection.update_one(
                            {
                                "_id": possible_transaction['_id']
                            },
                            {
                                "$set": {
                                    "status": "PARTIAL",
                                    "amount": "{}/{}".format(sell_amount,
                                                             total_sell_amount)
                                }
                            }
                        )
                    else:
                        self.collection.update_one(
                            {
                                "_id": possible_transaction['_id']
                            },
                            {
                                "$set": {
                                    "status": "PARTIAL",
                                    "amount": "{}/{}".format(sell_amount, total_sell_amount),
                                    "price": float(order["price"])
                                }
                            }
                        )
                self.history.insert_one({
                    "stock_name": order["stock_name"],
                    "price": float(order["price"])
                })
                self.collection.update_many(
                    {
                        "stock_name": order['stock_name'],
                        "order_type": "SELL",
                        "price": -1
                    },
                    {
                        "$set": {
                            "price": float(possible_transaction['price'])
                        }
                    }
                )
                amount_buy -= amount_bought
                self.__update_stop_loss(order['stock_name'], float(possible_transaction['price']))
                possible_transaction = self.collection.find_one(
                    {
                        "stock_name": order["stock_name"],
                        "order_type": "SELL",
                        "status": {
                            '$in': ["PENDING", "PARTIAL"]
                        },
                        "$or": [
                            {
                                "price": {
                                    '$lte': float(order["price"])
                                }
                            },
                            {
                                "price": {
                                    '$eq': -1
                                }
                            }
                        ]
                    }
                )
            if amount_buy == 0:
                total_amount_buy = curr_order['amount'].split('/')[-1]
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "FILLED",
                            "amount": "{}/{}".format(total_amount_buy,
                                                     total_amount_buy)
                        }
                    }
                )

    def __update_db_lmt_sell(self, order):
        """Perform database operations corresponding to SELL LMT command

        Arguments:
            order(dict): Dictionary with order info
        """
        self.collection.insert_one(order)
        curr_order, curr_order_id, curr_amount_sell = self.__get_curr_order()
        if self.__has_active_buy_orders(order):
            amount_sell = int(order['amount'].split('/')[-1])
            curr_amount_sell = int(curr_order['amount'].split('/')[0])
            possible_transaction = self.collection.find_one(
                {
                    "stock_name": order["stock_name"],
                    "order_type": "BUY",
                    "status": {
                        '$in': ["PENDING", "PARTIAL"]
                    },
                    "$or": [
                        {
                            "price": {
                                '$gte': float(order["price"])
                            }
                        },
                        {
                            "price": {
                                '$eq': -1
                            }
                        }
                    ]
                }
            )
            while possible_transaction is not None and amount_sell > 0:
                total_buy_amount = int(possible_transaction['amount'].split('/')[-1])
                curr_buy_amount = int(possible_transaction['amount'].split('/')[0])
                residual = total_buy_amount - curr_buy_amount
                amount_bought = min(amount_sell, residual)
                curr_amount_sell += amount_bought
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "PARTIAL",
                            "amount": "{}/{}".format(curr_amount_sell, amount_sell)
                        }
                    }
                )
                if amount_bought == residual:
                    self.collection.update_one(
                        {
                            "_id": possible_transaction['_id']
                        },
                        {
                            "$set": {
                                "status": "FILLED",
                                "amount": "{}/{}".format(total_buy_amount,
                                                         total_buy_amount),
                                "price": float(order['price'])
                            }
                        }
                    )
                else:
                    if possible_transaction["price_type"] == "LMT":
                        total_amount_sell = curr_buy_amount + amount_bought
                        self.collection.update_one(
                            {
                                "_id": possible_transaction['_id']
                            },
                            {
                                "$set": {
                                    "status": "PARTIAL",
                                    "amount": "{}/{}".format(total_amount_sell,
                                                             total_buy_amount)
                                }
                            }
                        )
                    else:
                        self.collection.update_one(
                            {
                                "_id": possible_transaction['_id']
                            },
                            {
                                "$set": {
                                    "status": "PARTIAL",
                                    "amount": "{}/{}".format(total_amount_sell,
                                                             total_buy_amount),
                                    "price": float(order["price"])
                                }
                            }
                        )
                self.history.insert_one({
                    "stock_name": order["stock_name"],
                    "price": float(order["price"])
                })
                self.collection.update_many(
                    {
                        "stock_name": order['stock_name'],
                        "order_type": "BUY",
                        "price": -1
                    },
                    {
                        "$set": {
                            "price": float(possible_transaction['price'])
                        }
                    }
                )
                amount_sell -= amount_bought
                self.__update_stop_loss(order['stock_name'], float(possible_transaction['price']))
                possible_transaction = self.collection.find_one(
                    {
                        "stock_name": order["stock_name"],
                        "order_type": "BUY",
                        "status": {
                            '$in': ["PENDING", "PARTIAL"]
                        },
                        "$or": [
                            {
                                "price": {
                                    '$gte': float(order["price"])
                                }
                            },
                            {
                                "price": {
                                    '$eq': -1
                                }
                            }
                        ]
                    }
                )
            if amount_sell == 0:
                total_sell_amount = curr_order['amount'].split('/')[-1]
                self.collection.update_one(
                    {
                        "_id": curr_order_id
                    },
                    {
                        "$set": {
                            "status": "FILLED",
                            "amount": "{}/{}".format(total_sell_amount,
                                                     total_sell_amount)
                        }
                    }
                )

    def __get_quote_prices(self, stock_name):
        """Get ask price, bid price and last transaction price for particular stock

        Arguments:
            stock_name(str): Name of stock to get info
        Returns:
            float, float, float: Bid price, ask price and last transaction price for stock
        """
        bid = self.collection.find_one(
            {
                "stock_name": stock_name,
                "order_type": "BUY",
                "status": {
                    '$in': ["PENDING", "PARTIAL"]
                }
            },
            sort=[("price", pymongo.ASCENDING)]
        )
        ask = self.collection.find_one(
            {
                "stock_name": stock_name,
                "order_type": "SELL",
                "status": {
                    '$in': ["PENDING", "PARTIAL"]
                }
            },
            sort=[("price", pymongo.ASCENDING)]
        )
        last = self.history.find_one(
            {
                "stock_name": stock_name
            },
            sort=[('_id', pymongo.DESCENDING)]
        )

        if bid is None or bid["price"] == -1:
            bid_price = 0
        else:
            bid_price = bid["price"]

        if ask is None or ask["price"] == -1:
            ask_price = 0
        else:
            ask_price = ask["price"]

        if last is None:
            last_price = 0
        else:
            last_price = last["price"]

        return bid_price, ask_price, last_price
