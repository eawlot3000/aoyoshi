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
    print(colored(f"Failed fetching product name from {url}. Error: {e}", "red"))
    return None



def existing_images_count(directory):
  existing_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
  image_files = [f for f in existing_files if f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']]
  return len(image_files)


def download_images(product_number, product_name):
  product_dir = os.path.join(os.getcwd(), product_name)

  if os.path.exists(product_dir): # Check if directory already exists
    print(colored(f"\nDirectory for '{product_name}' already exists. Moving to the next product...\n", "yellow"))
    return

  os.makedirs(product_dir, exist_ok=True)
    
  # Check existing images in the directory
  start_index = existing_images_count(product_dir) + 1
  consecutive_failed_attempts = 0  # Counter for consecutive failed download attempts

  for i in range(start_index, 11): 
    image_url = f"{IMAGE_BASE_URL}{product_number}/00/{i}_{BASE_URL[-10:]+product_number}.jpg"
    
    try:
      response = requests.get(image_url, stream=True)
      response.raise_for_status()
      with open(os.path.join(product_dir, f"{i}.jpg"), 'wb') as out_file:
        for chunk in response.iter_content(1024):
          out_file.write(chunk)
        print(colored(f"\n>>> {i}.jpg downloaded successfully to >> {product_name}\n", "green"))
        consecutive_failed_attempts = 0  # Reset counter after a successful download
    except Exception as e:
      print(colored(f"Failed fetching image from {image_url}. Error: {e}\n", "red"))
      consecutive_failed_attempts += 1
      if consecutive_failed_attempts == 2:  # If two consecutive images are not available, break out of loop
        break



def main():
  print("\n==================== Starting downloading...====================\n")
  
  processed_products = set()  # Set to remember processed product names
  
  for i in range(1000, 10000000000): #TODO
    url = BASE_URL + str(i).zfill(10)
    response = requests.head(url)
        
    if response.status_code == 200:
      product_name = get_product_name(url)
      print("============================================================\n> Working with: ", product_name)
      if product_name and product_name not in processed_products: # set() is used to avoid duplicate downloads
        download_images(str(i).zfill(2), product_name)
        processed_products.add(product_name)  # Add to set after processing
    else:
      print(colored(f"{url} is not valid. Skipping...", "red"))



if __name__ == "__main__":
  main()
