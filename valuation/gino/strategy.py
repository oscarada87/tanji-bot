'''
在沒有淡旺季產業、每季營收維持一樣的狀態下
完整估價計算:
(((當月營收 * 3 * 毛利率) - 營業費用 + 業外收益) * (1 - 稅率)) / 股本) * 4 * 本益比 = 預估股價

拆項:
當月營收 * 3 = 單季預估營收
單季預估營收 * 毛利率 = 單季預估毛利
單季預估毛利 - 單季營業費用 + 單季業外收益 = 單季稅前淨利
單季稅前淨利 * (1 - 稅率) = 單季稅後淨利 
單季稅後淨利 / 股本 = 單季預估 EPS
單季預估 EPS * 4 = 年預估 EPS
年預估 EPS * 預估本益比 = 預估股價
'''

class GinoStrategy:
  def execute(self, stock_id):
    self.stock_id = stock_id

  def find_newest_revenue(self):
    pass

  def calculate_estimate_price(self):
    gross_profit = self.revenue * 3 * self.gross_margin # 單季預估毛利
    profit_before_tax = gross_profit - self.operating_expense + self.non_operating_earning
    profit_after_tax = profit_before_tax * (1 - self.tax_rate)
    eps_per_season = profit_after_tax / self.share_capital
    eps = eps_per_season * self.year_ratio
    stock_price = eps * self.p_e_ratio