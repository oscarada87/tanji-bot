from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, element
from flask import current_app

class RevenueCrawler:
  def __init__(self, stock_id):
    self.url = 'https://mops.twse.com.tw/mops/web/t05st10_ifrs'
    self.stock_id = stock_id
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    self.browser = webdriver.Chrome(options=options)

  def send(self):
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # options.binary_location = current_app.config['GOOGLE_CHROME_BIN']
    # browser = webdriver.Chrome(executable_path=current_app.config['CHROMEDRIVER_PATH'], chrome_options=options)
    self.browser.get(self.url)
    self.browser.find_element(By.ID, 'co_id').send_keys(self.stock_id)
    self.browser.find_element(By.XPATH, "//input[@value=' 查詢 ']").click()
    delay = 3 # seconds
    try:
      self.browser.find_element(By.XPATH, "//*[contains(text(), '查無最新資訊')]")
      return "{} 查無最新營收資訊".format(self.stock_id)
    except NoSuchElementException:
      pass

    self.browser.save_screenshot('screenshot.png')
    revenue = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="table01"]/table[4]/tbody/tr[2]/td'))).text.replace(' ', '') + ' 元'#.replace(',', '')
    date = self.browser.find_element(By.XPATH, '//*[@id="table01"]/table[3]/tbody/tr/td[2]').text
    name = self.browser.find_element(By.XPATH, '//*[@id="table01"]/table[2]/tbody/tr/td/b').text.split('\u3000')[1]
    self.tearDown()
    msg = str.join('\n', ["公司名稱: " + name, "時間: " + date,"營收: " + revenue])
    return msg

  def tearDown(self):
    """Stop web driver"""
    self.browser.quit()

  
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
