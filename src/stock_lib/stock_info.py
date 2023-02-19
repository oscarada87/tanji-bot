import os
from dotenv import load_dotenv
from fugle_realtime import HttpClient

class StockInfo:
    def __init__(self):
        load_dotenv()
        self.api = HttpClient(api_token = os.getenv('FUGLE_TOKEN'))

    def margin_purchase(self, stock_id):
        data = self.api.intraday.quote(symbolId = stock_id)
        latest_price = data['data']['quote']['trade']['price']
        data = MarginPurchase()
        data.stock_id = stock_id
        data.latest_price = latest_price
        return data

# 融資
class MarginPurchase:
    # 股票代碼
    @property
    def stock_id(self):
        return self._stock_id
    @stock_id.setter
    def stock_id(self, value):
        self._stock_id = value
    
    # 最後成交價
    @property
    def latest_price(self):
        return self._latest_price
    @latest_price.setter
    def latest_price(self, value):
        self._latest_price = value

    # 一張自付額
    def deductible(self):
        return round(self._latest_price * 0.4 * 1000)

    # 一張借貸額
    def loan(self):
        return round(self._latest_price * 0.6 * 1000)

    # 利息 (天)
    def interest(self):
        return round((self.loan() * 0.06275) / 365, 2)

    # 斷頭價 (維持率不足 130 %)
    def warning_price(self):
        return round(self._latest_price * 0.6 * 1.3, 2)

    def message(self):
        msg_list = []
        msg_list.append("股票代碼: " + str(self._stock_id))
        msg_list.append("最新收盤價: " + str(self._latest_price))
        msg_list.append("自付額: " + str(self.deductible()))
        msg_list.append("借貸額: " + str(self.loan()))
        msg_list.append("一天利息: " + str(self.interest()))
        msg_list.append("斷頭價: " + str(self.warning_price()))
        return str.join('\n', msg_list)