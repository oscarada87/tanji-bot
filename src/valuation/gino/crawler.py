from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
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
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(options=options)

    def send(self):
        self.browser.get(self.url)
        self.browser.find_element(By.ID, 'co_id').send_keys(self.stock_id)
        self.browser.find_element(By.XPATH, "//input[@value=' 查詢 ']").click()
        delay = 3  # seconds
        try:
            month_revenue = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="table01"]/table[4]/tbody/tr[2]/td'))).text.replace(' ', '') + ',000'
            month_revenue_percentage = self.browser.find_element(
                By.XPATH, '//*[@id="table01"]/table[4]/tbody/tr[5]/td').text.replace(' ', '')
            if '-' in month_revenue_percentage:
                month_revenue_percentage = '📉 ' + month_revenue_percentage
            else:
                month_revenue_percentage = '📈 ' + month_revenue_percentage
            year_revenue = self.browser.find_element(
                By.XPATH, '//*[@id="table01"]/table[4]/tbody/tr[6]/td').text.replace(' ', '') + ',000'
            year_revenue_percentage = self.browser.find_element(
                By.XPATH, '//*[@id="table01"]/table[4]/tbody/tr[9]/td').text.replace(' ', '')
            if '-' in year_revenue_percentage:
                year_revenue_percentage = '📉 ' + year_revenue_percentage
            else:
                year_revenue_percentage = '📈 ' + year_revenue_percentage
            date = self.browser.find_element(
                By.XPATH, '//*[@id="table01"]/table[3]/tbody/tr/td[2]').text
            name = self.browser.find_element(
                By.XPATH, '//*[@id="table01"]/table[2]/tbody/tr/td/b').text.split('\u3000')[1]
            self.tearDown()
            msg = str.join('\n', [
                '公司名稱: ' + name,
                '時間: ' + date,
                '本月營收: ' + month_revenue + ' 元',
                '本月較同期增減百分比: ' + month_revenue_percentage + ' %',
                '今年營收累積: ' + year_revenue + ' 元',
                '今年營收累積較同期增減百分比: ' + year_revenue_percentage + ' %'
            ]
            )
            return msg
        except Exception as e:
            return "{} 查無最新營收資訊".format(self.stock_id)

    def tearDown(self):
        """Stop web driver"""
        self.browser.quit()


if __name__ == '__main__':
    a = RevenueCrawler(2330)
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
