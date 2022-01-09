from flask_sqlalchemy import SQLAlchemy
from .models import Stock, AfterHourInformation
from datetime import datetime
import requests

class TwStockCrawler:
    def run(self):
        self.grab_daily_tw_stock_info()
        self.grab_daily_tw_otc_info()

    def __init__(self):
        self.db = SQLAlchemy()
        self.tw_stock_url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json'
        self.tw_otc_url = 'https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes'

    def grab_daily_tw_stock_info(self):
        r = requests.get(self.tw_stock_url)
        data = r.json()
        data_date = datetime.strptime(data['date'], "%Y%m%d").date()
        for item in data['data']:
            stock_code = item[0]
            stock = Stock.query.filter_by(code=stock_code).first()
            if stock is None:
                stock = Stock(code=stock_code, name=item[1], updated_at=datetime.now())
                self.db.session.add(stock)
                self.db.session.commit()
            daily_info = self.db.session.query(AfterHourInformation).filter_by(stock_id=stock.id).first()
            if daily_info is None:
                daily_info = AfterHourInformation(
                    stock_id = stock.id,
                    max = self.__convert_to_float(item[5]),
                    min = self.__convert_to_float(item[6]),
                    open = self.__convert_to_float(item[4]),
                    close = self.__convert_to_float(item[7]),
                    spread = self.__convert_to_float(item[8]),
                    trading_volume = item[2],
                    trading_money = item[3],
                    trading_turnover = item[9],
                    current_date = data_date,
                )
                self.db.session.add(daily_info)
                self.db.session.commit()
            elif daily_info.current_date != data_date:
                daily_info.max = self.__convert_to_float(item[5])
                daily_info.min = self.__convert_to_float(item[6])
                daily_info.open = self.__convert_to_float(item[4])
                daily_info.close = self.__convert_to_float(item[7])
                daily_info.spread = self.__convert_to_float(item[8])
                daily_info.trading_volume = item[2]
                daily_info.trading_money = item[3]
                daily_info.trading_turnover = item[9]
                daily_info.current_date = data_date
                self.db.session.commit()
                
    def grab_daily_tw_otc_info(self):
        r = requests.get(self.tw_otc_url)
        data = r.json()
        date_string = str(int(data[0]['Date'][:3]) + 1911) + data[0]['Date'][3:]
        data_date = datetime.strptime(date_string, "%Y%m%d").date()
        for item in data:
            stock_code = item['SecuritiesCompanyCode']
            stock = Stock.query.filter_by(code=stock_code).first()
            if stock is None:
                stock = Stock(code=stock_code, name=item['CompanyName'], updated_at=datetime.now())
                self.db.session.add(stock)
                self.db.session.commit()
            daily_info = self.db.session.query(AfterHourInformation).filter_by(stock_id=stock.id).first()
            if daily_info is None:
                daily_info = AfterHourInformation(
                    stock_id = stock.id,
                    max = self.__convert_to_float(item['High']),
                    min = self.__convert_to_float(item['Low']),
                    open = self.__convert_to_float(item['Open']),
                    close = self.__convert_to_float(item['Close']),
                    spread = self.__convert_to_float(item['Change']),
                    trading_volume = item['TradingShares'],
                    trading_money = item['TransactionAmount'],
                    trading_turnover = item['TransactionNumber'],
                    current_date = data_date,
                )
                self.db.session.add(daily_info)
                self.db.session.commit()
    
    def __convert_to_float(self, val):
        try:
            return float(val)
        except ValueError:
            return 0.0
