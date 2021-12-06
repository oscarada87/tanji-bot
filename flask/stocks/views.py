from . import stock
from .models import Stock, AfterHourInformation
from .tw_stock_worker import TwStockWorker
from datetime import date
from flask import jsonify

@stock.route('/')
def stock_index():
    # a = TwStockWorker()
    # a.grab_daily_info()
    stocks = Stock.query.limit(10).all()
    # temp = Stock(id=6170, name='統振', industry_category='通信網路類', updated_at=datetime.now())
    # db.session.add(temp)
    # db.session.commit()
    # breakpoint()
    return jsonify(stocks)


@stock.route('/daily/')
def dialy_index():
    stocks = AfterHourInformation.query.limit(10).all()
    return jsonify(stocks)