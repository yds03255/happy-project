from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chrome_path = 'C:/Users/윤혜준/Desktop/chromedriver'
driver = webdriver.Chrome(chrome_path)
url = 'http://browse.auction.co.kr/search?keyword=%ed%9b%84%eb%9d%bc%ec%9d%b4%ed%8c%ac&itemno=&nickname=&frm=hometab&dom=auction&isSuggestion=No&retry=&Fwk=%ed%9b%84%eb%9d%bc%ec%9d%b4%ed%8c%ac&acode=SRP_SU_0100&arraycategory=&encKeyword=%ed%9b%84%eb%9d%bc%ec%9d%b4%ed%8c%ac&s=8'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
pans = soup.select("#section--inner_content_body_container > div:nth-child(2) > div")
ls = []
for pan in pans:
    a_tag = pan.select_one("div.itemcard > div > div.section--itemcard_info > div.section--itemcard_info_major")
    if a_tag is not None:
        name = pan.select_one("div.area--itemcard_title > span").text
        price = pan.select_one("div.area--itemcard_price > span.price_seller > strong").text.replace(',', '')
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
    'market': 'auction'
}
db.price.insert_one(doc)