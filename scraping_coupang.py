from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chrome_path = 'C:/Users/윤혜준/Desktop/chromedriver'
driver = webdriver.Chrome(chrome_path)
url = 'https://www.coupang.com/np/search?q=%ED%9B%84%EB%9D%BC%EC%9D%B4%ED%8C%AC&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=72'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
pans = soup.select("dl.search-product-wrap")
ls = []
for pan in pans:
    a_tag = pan.select_one("div")
    if a_tag is not None:
        name = pan.select_one("div.name").text
        price = pan.select_one("strong.price-value").text.replace(',', '')
        price = int(price)
        ls.append({
            'name': name,
            'price': price
        })
        print(name, price, sep='\t')
driver.quit()
# ls = list(db.prices.find({}))
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
    'market': 'coupang'
}
db.price.insert_one(doc)