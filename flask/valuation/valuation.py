from enum import Enum

class valuation:
  def __init__(self, stock_id):
      self.stock_id = stock_id

  def set_strategy(self, strategy):
    self.strategy = strategy


class StrategyType(Enum):
  GINO = 'GINO'

if __name__ == '__main__':
  pass