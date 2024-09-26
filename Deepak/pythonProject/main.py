import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Headers for the request
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

for i in range(2, 7):
    url = "https://www.flipkart.com/search?q=lipstick&sid=g9b%2Cffi%2Ctv5%2Cuna&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=lipstick%7CLipstick&requestId=4c0d77db-c7dd-4574-b075-a1cb15d53e32&as-backfill=on&page=" + str(i)

    # Send a GET request with headers
    r = session.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="DOjaWF gdgoEp")

    if box:
        names = box.find_all("a", class_="wjcEIp")
        prices = box.find_all("div", class_="Nx9bqj")
        mrps = box.find_all("div", class_="yRaY8j")
        reviews = box.find_all("div", class_="XQDdHH")

        for name, price, mrp, review in zip(names, prices, mrps, reviews):
            Product_Name.append(name.text)
            Prices.append(price.text)
            MRP.append(mrp.text if mrp else price.text)
            Reviews.append(review.text if review else '0')

            prod_url = name.get("href")
            if prod_url:
                links = "https://www.flipkart.com" + prod_url
                Link.append(links)

# Handle any length mismatches (if any)
min_length = min(len(Product_Name), len(Prices), len(MRP), len(Reviews), len(Link))

# Slice lists to the minimum length
Product_Name = Product_Name[:min_length]
Prices = Prices[:min_length]
MRP = MRP[:min_length]
Reviews = Reviews[:min_length]
Link = Link[:min_length]

# Create DataFrame
df = pd.DataFrame({"Product Name": Product_Name, "Price": Prices, "MRP Value": MRP, "Rating": Reviews, "URLs": Link})

# Generate filename with current date and time
now = datetime.now()
filename = now.strftime("Lipstick_%d%m%y_%H%M.xlsx")

# Specify the path
file_path = r"C:\Users\Deepak Prajapati\Desktop\Deepak\\" + filename

# Save the DataFrame to Excel
df.to_excel(file_path, index=False)

print(f"Data saved to {file_path}")
