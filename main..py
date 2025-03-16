import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()

products = []
actual_prices=[]
discount_prices =[]
ratings = []

base_url = "https://www.flipkart.com"
driver.get("https://www.flipkart.com/search?p%5B%5D=facets.brand%255B%255D%3DSamsung&sid=tyy%2F4io&sort=recency_desc&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkxhdGVzdCBTYW1zdW5nIG1vYmlsZXMgIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D&wid=1.productCard.PMU_V2_1")


while True:
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    for a in soup.find_all('a', href=True,attrs={'class':'CGtC98'}):
        name = a.find('div',attrs={'class':'KzDlHZ'})
        actual_price = a.find('div',attrs={'class':'yRaY8j ZYYwLA'})
        discount_price = a.find('div',attrs={'class':'Nx9bqj _4b5DiR'})
        rating = a.find('div',attrs={'class':'XQDdHH'})

        if name and actual_price and discount_price:
            products.append(name.text)
            actual_prices.append(actual_price.text)
            discount_prices.append(discount_price.text)
            ratings.append(rating.text if rating else "N/A")

    next_button = soup.find('a',string="Next")
    if next_button and 'href' in next_button.attrs:
        next_page_url = base_url + next_button['href']
        print(f"Navigating to: {next_page_url}")
        driver.get(next_page_url)
    else:
        print("No more page. Scraping completed.")
        break

driver.quit()


df = pd.DataFrame({'Products':products,'Actual Prices':actual_prices,'Discount Prices':discount_prices,'Ratings':ratings})
df.to_csv('products.csv',index=False,encoding='utf-8')
print("Data saved to products.csv")

