import pandas as pd
import requests
from bs4 import BeautifulSoup

# url = "https://www.flipkart.com/search?q=lipstick&sid=g9b%2Cffi%2Ctv5%2Cuna&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=lipstick%7CLipstick&requestId=4c0d77db-c7dd-4574-b075-a1cb15d53e32&as-backfill=on&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

# Initialize a session
session = requests.Session()

Product_Name = []
Prices = []
MRP = []
Reviews = []
Link = []

for i in range(2,7):
    url = "https://www.flipkart.com/search?q=lipstick&sid=g9b%2Cffi%2Ctv5%2Cuna&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=lipstick%7CLipstick&requestId=4c0d77db-c7dd-4574-b075-a1cb15d53e32&as-backfill=on&page="+str(i)

    # Send a GET request with headers
    r = session.get(url, headers=headers)

    # print(r)

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_ = "DOjaWF gdgoEp")

    # print(soup)

    names = box.find_all("a", class_ = "wjcEIp")

    for i in names:
        name = i.text
        Product_Name.append(name)
    # print(Product_Name)

    prices = box.find_all("div", class_ = "Nx9bqj")

    for i in prices:
        price = i.text
        Prices.append(price)
    # print(Prices)

    mrps = box.find_all("div", class_ = "yRaY8j")
    for i in mrps:
        mrp = i.text
        MRP.append(mrp)
    # print(MRP)

    reviews = box.find_all("div", class_ = "XQDdHH")
    for i in reviews:
        review = i.text
        Reviews.append(review)
    # print(Reviews)

    prod_url = box.find("a", class_ = "wjcEIp").get("href")
    links = "https://www.flipkart.com"+prod_url
    for i in links:
        link = links
        Link.append(link)
    # print(Link)

df = pd.DataFrame({"Product Name":Product_Name,"Price":Prices,"MRP Value": MRP,"Rating":Reviews,"URLs":Link})
print(df)