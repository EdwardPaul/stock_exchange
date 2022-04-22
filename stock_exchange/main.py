from stock_exchange.cli import ConsoleInterface
from stock_exchange.repository.mongorepo import MongoRepo

if __name__ == '__main__':
    repo = MongoRepo()
    cli = ConsoleInterface(repo)
    cli.run()
