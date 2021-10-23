from . import stock
from .models import Stock
from datetime import datetime
from flask import jsonify
from app import db

@stock.route('/')
def index():
    stocks = Stock.query.limit(10).all()
    # temp = Stock(id=6170, name='統振', industry_category='通信網路類', updated_at=datetime.now())
    # db.session.add(temp)
    # db.session.commit()
    # breakpoint()
    return jsonify(stocks)