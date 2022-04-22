# stock_exchange
A simple stock exchange CLI python program inspired by Robert Martin's "Clean Architecture".

# Prerequisites
- Python 3.
- MongoDB 5.0

# Installation
1. Clone repository:
`git clone https://github.com/EdwardPaul/stock_exchange.git`
2. Install requirements:
`pip install -r requirements.txt`
3. Build and install python project:
``` 
python3 setup.py build
sudo python3 setup.py install
```

# Launch

Launch app:
``` 
python3 stock_exchange/main.py
```

Launch tests:
```
pytest -sv
```

# Commands
- `BUY {STOCK_NAME} MKT {AMOUNT} `: Place buy order of {AMOUNT} of {STOCK_NAME} stocks.
- `SELL {STOCK_NAME} MKT {AMOUNT} `: Place sell order of {AMOUNT} of {STOCK_NAME} stocks.
- `BUY {STOCK_NAME} LMT {PRICE} {AMOUNT} `: Place buy order of {AMOUNT} of {STOCK_NAME} stocks at {PRICE} each.
- `SELL {STOCK_NAME} LMT {PRICE} {AMOUNT} `: Place sell order of {AMOUNT} of {STOCK_NAME} stocks at {PRICE} each.
- `VIEW ORDERS`: View all orders made during current client session.
- `QUOTE {STOCK_NAME}`: View ask price, bid price and price of last transaction for {STOCK_NAME}
- `QUIT`: Quit program
