# from app import db
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime

db = SQLAlchemy()

@dataclass
class Stock(db.Model):
    __tablename__ = 'stocks'
    id: int  # 股票代碼
    name: str  # 股票名稱
    updated_at: datetime  # 更新時間

    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True)
    name = db.Column(db.String(10), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, nullable=False) 
    after_hour_information = db.relationship('AfterHourInformation', uselist=False, backref='stock')


@dataclass
class AfterHourInformation(db.Model):
    stock_id: int  # 股票代碼
    max: float  # 今日最高價
    min: float  # 今日最低價
    open: float  # 今日開盤價
    close: float  # 今日收盤價
    spread: float  # 今日漲跌價差
    trading_volume: str  # 今日交易量
    trading_money: str  # 今日交易金額
    trading_turnover: str  # 今日交易筆數
    current_date: datetime.date  # 今日日期

    __tablename__ = 'stocks_after_hour_information'
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False, primary_key=True, index=True)
    max = db.Column(db.Float)
    min = db.Column(db.Float)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    spread = db.Column(db.Float)
    trading_volume = db.Column(db.String(100))
    trading_money = db.Column(db.String(100))
    trading_turnover = db.Column(db.String(100))
    current_date = db.Column(db.Date, nullable=False)

    def percentage(self):
        round((self.spread/self.close) * 100, 2)