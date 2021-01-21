from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chrome_path = 'C:/Users/윤혜준/Desktop/chromedriver'
driver = webdriver.Chrome(chrome_path)
url = 'https://search.shopping.naver.com/search/all?query=%ED%9B%84%EB%9D%BC%EC%9D%B4%ED%8C%AC&cat_id=&frm=NVSHATC'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
pans = soup.select(
    "#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div ")
ls = []
for pan in pans:
    a_tag = pan.select_one("li > div > div.basicList_info_area__17Xyo")
    if a_tag is not None:
        try:
            # li[class^="basicList_item"] > div[class^="basicList_inner"] > ...
            ##__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(1) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a
            name = pan.select_one("div.basicList_title__3P9Q7 > a ").text
        except Exception:
            name = ''
        try:
            price = pan.select_one("div.basicList_price_area__1UXXR > strong").text.replace('원', '').replace(',', '')
        except Exception:
            price = ''
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
    'market': 'naver'
}
db.price.insert_one(doc)
