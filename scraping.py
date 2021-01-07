import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(
    'https://search.11st.co.kr/Search.tmall?kwd=%25ED%259B%2584%25EB%259D%25BC%25EC%259D%25B4%25ED%258C%25AC#sortCd%%SPS%%11%EB%B2%88%EA%B0%80%20%EC%9D%B8%EA%B8%B0%EC%88%9C%%1',
    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

pans = soup.select("#contsWrap > div > section:nth-child(3) > ul > li")

for pan in pans:
    a_tag = pan.select_one("div")
    if a_tag is not None:
        name = pan.select_one("div:nth-child(2) > div.c_card_info_top > div.c_prd_name.c_prd_name_row_1").text
        price = pan.select_one("div:nth-child(2) > div.c_card_info_top > div.c_prd_price").text
        brand = pan.select_one("div:nth-child(3) > div.c_prd_seller").text

        print(name, price, brand)
