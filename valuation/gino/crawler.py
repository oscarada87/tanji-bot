from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, element
from flask import current_app

class RevenueCrawler:
  def __init__(self, stock_id):
    self.url = 'https://mops.twse.com.tw/mops/web/t05st10_ifrs'
    self.stock_id = stock_id

  def send(self):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = current_app.config['GOOGLE_CHROME_BIN']
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    browser = webdriver.Chrome(executable_path=current_app.config['CHROMEDRIVER_PATH'], chrome_options=options)
    browser.get(self.url)
    browser.find_element(By.ID, 'co_id').send_keys(self.stock_id)
    browser.find_element(By.XPATH, "//input[@value=' 查詢 ']").click()
    try:
      element = browser.find_element(By.XPATH, "//*[contains(text(), '查無最新資訊')]")
      return "{} 查無最新營收資訊".format(self.stock_id)
    except NoSuchElementException:
      pass
      
    browser.save_screenshot('screenshot.png')
    revenue = browser.find_element(By.CSS_SELECTOR, '#table01 > table.hasBorder > tbody > tr:nth-child(2) > td').text.replace(' ', '') + ' 元'#.replace(',', '')
    date = browser.find_element(By.CSS_SELECTOR, '#table01 > table:nth-child(5) > tbody > tr > td:nth-child(2)').text
    name = browser.find_element(By.CSS_SELECTOR, '#table01 > table:nth-child(4) > tbody > tr > td > b').text.split('\u3000')[1]
    msg = str.join('\n', ["公司名稱: " + name, "時間: " + date,"營收: " + revenue])
    return msg

  
if __name__ == '__main__':
  a = RevenueCrawler(2376)
  temp = a.send()
  print(temp)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup

# url = 'https://www.cmoney.tw/finance/f00043.aspx?s=2376'
# options = Options()
# options.add_argument("--disable-notifications")
# # options.add_argument("--headless")
# # options.add_argument("--window-size=1920,1080")
# browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
# browser.get(url)
# parent = browser.find_element(By.CSS_SELECTOR , "#MainContent > ul > li:nth-child(2) > article > div > div > div > table")
# table = parent.find_elements(By.XPATH, './/tr')

# #MainContent > ul > li:nth-child(2) > article > div > div > div > table
