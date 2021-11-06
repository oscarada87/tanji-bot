from ..models import Stock, DailyInformation
from flask import current_app
import twstock
from app import db


class GrabDailyInfoJob:
    def __init__(self):
        self.api = twstock

    def grab(self):
        self.get_stock_list()
        self.save_stocks()

    def get_stock_list(self):
        self.stocks = Stock.query.all()

    def save_stocks(self):
        for stock in self.stocks:
            try:
                stock_info = twstock.Stock(str(stock.id))
                daily_info = self.retrieve_daily_info(stock.id)
                daily_info.stock_id = stock.id
                daily_info.max = stock_info.high[-1]
                daily_info.min = stock_info.low[-1]
                daily_info.open = stock_info.open[-1]
                daily_info.close = stock_info.close[-1]
                daily_info.spread = stock_info.change[-1]
                daily_info.trading_volume = str(stock_info.capacity[-1])
                daily_info.trading_money = str(stock_info.turnover[-1])
                daily_info.trading_turnover = str(stock_info.transaction[-1])
                daily_info.current_date = stock_info.date[-1].date()
                breakpoint()
                db.session.commit()
            except:
                next
        # breakpoint()

    def retrieve_daily_info(self, stock_id):
        daily_info = DailyInformation.query.get(stock_id)
        if daily_info is None:
            daily_info = DailyInformation()
            current_app.db.session.add(daily_info)
        return daily_info
