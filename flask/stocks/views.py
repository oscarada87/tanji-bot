from . import stock
from .models import Stock, AfterHourInformation
from flask import jsonify

@stock.route('/')
def stock_index():
    stocks = Stock.query.limit(10).all()

    return jsonify(stocks)


@stock.route('/daily/')
def dialy_index():
    stocks = AfterHourInformation.query.limit(10).all()
    return jsonify(stocks)