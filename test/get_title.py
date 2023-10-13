#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def get_product_name(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch the URL!")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    item_detail = soup.find(class_='item-detail')
    
    if not item_detail:
        print("Couldn't find the 'item-detail' class!")
        return
    
    h2_tag = item_detail.find('h2')
    
    if not h2_tag:
        print("Couldn't find an <h2> tag inside 'item-detail'!")
        return

    print(h2_tag.text)

# Replace with the desired product URL
# url = "https://www.blackvintageinox.com/shopdetail/000000000075"
url = str(input("Enter the URL: "))
get_product_name(url)

