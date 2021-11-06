from . import stock
from .models import Stock, DailyInformation
# from .jobs.grab_daily_info import GrabDailyInfoJob
from datetime import date
from flask import jsonify
from app import db


@stock.route('/')
def stock_index():
    stocks = Stock.query.limit(10).all()
    # temp = Stock(id=6170, name='統振', industry_category='通信網路類', updated_at=datetime.now())
    # db.session.add(temp)
    # db.session.commit()
    # breakpoint()
    return jsonify(stocks)


@stock.route('/daily/')
def dialy_index():
    stocks = DailyInformation.query.limit(10).all()
    # temp = DailyInformation(
    #     stock_id=6170,
    #     max=43.15,
    #     min=42,
    #     open=42,
    #     close=43.05,
    #     spread=1.05,
    #     trading_volume=1344000,
    #     trading_money=57185650,
    #     trading_turnover=851,
    #     current_date=date.fromisoformat('2021-10-22')
    #     )
    # a = GrabDailyInfoJob()
    # a.grab()
    return jsonify(stocks)