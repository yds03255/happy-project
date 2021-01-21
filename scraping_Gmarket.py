from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chromedriver = 'C:/Users/윤혜준/Desktop/chromedriver'
driver = webdriver.Chrome(chromedriver)
url = 'https://browse.gmarket.co.kr/search?keyword=%ed%9b%84%eb%9d%bc%ec%9d%b4%ed%8c%ac&s=8'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# section__inner-content-body-container > div:nth-child(2) > div:nth-child(1)
# section__inner-content-body-container > div:nth-child(2) > div:nth-child(2)
# section__inner-content-body-container > div:nth-child(2) > div:nth-child(3)
pans = soup.select("#section__inner-content-body-container > div:nth-child(2) > div")
ls = []
for pan in pans:
    a_tag = pan.select_one("div.box__information > div.box__information-major")
    if a_tag is not None:
        name = pan.select_one("div.box__item-title > span > a > span.text__item").text
        price = pan.select_one("div.box__item-price > div.box__price-seller > strong.text__value").text.replace(',','')
        price = int(price)
        try:
            brand = pan.select_one("div.box__item-title > span > a > span.text__brand").text
        except Exception:
            brand = ''
            price = int(price)
            ls.append({
                'price': price
            })
            print(name, price, brand, sep='\t')
driver.quit()
prices = [t['price'] for t in ls]
prices_sum = sum(prices)
min = min(prices)
max = max(prices)
avg = prices_sum / len(prices)
print(avg, min, max)

doc = {
    'avg': avg,
    'max': max,
    'min': min,
    'market': 'Gmarket'
}
db.price.insert_one(doc)
