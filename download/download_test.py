#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored # print color


BASE_URL = "https://www.blackvintageinox.com/shopdetail/0000000000"
IMAGE_BASE_URL = "https://makeshop-multi-images.akamaized.net/blackvintage/shopimages/"

def get_product_name(url):
  try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    item_detail = soup.find(class_='item-detail')
    if not item_detail:
      return None
    h2_tag = item_detail.find('h2')
    if not h2_tag:
      return None
    return h2_tag.text
  except Exception as e:
    print(f"Failed fetching product name from {url}. Error: {e}")
    return None

def download_images(product_number, product_name):
  product_dir = os.path.join(os.getcwd(), product_name)
  os.makedirs(product_dir, exist_ok=True)
    
  for i in range(1, 11): #TODO: change iteration!!
    image_url = f"{IMAGE_BASE_URL}{product_number}/00/{i}_{BASE_URL[-10:]+product_number}.jpg"

    try:
      response = requests.get(image_url, stream=True)
      response.raise_for_status()
            
      with open(os.path.join(product_dir, f"{i}.jpg"), 'wb') as out_file:
        for chunk in response.iter_content(1024):
          out_file.write(chunk)
        print(f"\n>>> {i}.jpg downloaded successfully to >> {product_dir}\n")

    except Exception as e:
      print(f"Failed fetching image from {image_url}. Error: {e}\n")

def main():
  time.sleep(5)
  print("\nStarting downloading...\n========================================\n")
  for i in range(1, 3): # TODO: change iteration!!
    url = BASE_URL + str(i).zfill(2)
    response = requests.head(url)  # This is to mimic the curl -I command
        
    if response.status_code == 200:
      product_name = get_product_name(url)
      print(">Working with: ", product_name)
      if product_name:
        download_images(str(i).zfill(2), product_name)
    else:
      print(f"{url} is not valid. Skipping...")

if __name__ == "__main__":
  main()
