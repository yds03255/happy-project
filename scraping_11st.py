from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chromedriver = 'C:/Users/윤혜준/Desktop/chromedriver'
driver = webdriver.Chrome(chromedriver)
url = 'https://search.11st.co.kr/Search.tmall?kwd=%25ED%259B%2584%25EB%259D%25BC%25EC%259D%25B4%25ED%258C%25AC#sortCd%%SPS%%11%EB%B2%88%EA%B0%80%20%EC%9D%B8%EA%B8%B0%EC%88%9C%%1'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

pans = soup.select("#contsWrap > div > section:nth-child(3) > ul > li")
ls = []
for pan in pans:
    a_tag = pan.select_one("div")
    if a_tag is not None:
        try:
            name = pan.select_one("div:nth-child(2) > div.c_card_info_top > div.c_prd_name.c_prd_name_row_1").text
        except Exception:
            name = ''
        try:
            price = pan.select_one("div:nth-child(2) > div.c_card_info_top > div.c_prd_price").text[3:10].replace('원',
                                                                                                                  '')
        except Exception:
            price = ''
            price = int(price)
        try:
            brand = pan.select_one("div:nth-child(3) > div.c_prd_seller").text
        except Exception:
            brand = ''
ls.append({
    'name': name, 'brand': brand, 'price': price})
print(name, price, brand, sep='\t')
driver.quit()
prices = [t['price'] for t in ls]
min = min(prices)
max = max(prices)
prices_sum = sum(prices)
avg = prices_sum / len(prices)
print(avg)
doc = {
    'avg': avg,
    'max': max,
    'min': min,
    'market': '11st'
}
db.price.insert_one(doc)
