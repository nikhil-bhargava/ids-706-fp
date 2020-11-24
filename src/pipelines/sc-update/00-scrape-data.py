# import packages
from bs4 import BeautifulSoup
import requests
import re
import json
from ast import literal_eval
import json
import urllib.request
import numpy as np
import pandas as pd
import time
import datetime
import random
import os
from pathlib import Path

# create data storage
end = False
solecollector_com = 'https://solecollector.com'
textify = lambda x: x.text
stripify = lambda x: x.strip()
sneaker_keys = ['id', 'name', 'date_created', 'date_updated', 'alias', 'release_date', 'images', 
                'description', 'style_code', 'original_price', 'hero_image', 'available_at', 'url', 
                'release_day', 'release_month', 'hero_image_url', 'hero_image_id', 'release_date_pretty', 
                'original_price_pretty', 'hero_image_alt', 'canonical_url']

sneaker_json = []
brand_json = []
secondary_brand_json = []
silhouette_json = []

# generate current month url
year = datetime.datetime.now().year
month = datetime.datetime.now().month
urls = f'https://solecollector.com/sneaker-release-dates/all-release-dates/{year}/{month}/'

# collect data
def get_data(sneaker_soup, sneaker_script):
    
    # Obtain data on brand, secondary brand, and silhouette
    no_additional_data = False
    query1 = re.search('var sneaker_path = (.+)[,;]{1}', sneaker_script)
    if query1:
        query1_data = json.loads(query1.group(1))
        
        brand = query1_data[0]
        secondary_brand = query1_data[1]
        silhouette = query1_data[2]
        
        brand_id = brand['id']
        secondary_brand_id = secondary_brand['id']
        silhouette_id = silhouette['id']
        
    else:
        
        no_additional_data = True
        brand_id = np.nan
        secondary_brand_id = np.nan
        silhouette_id = np.nan
    
    # Obtain data on sneaker
    query2 = re.search('var sneaker_release = (.+)[,;]{1}', sneaker_script)
    if query2:
        sneaker = json.loads(query2.group(1))
        sneaker['brand_id'] = brand_id
        sneaker['secondary_brand_id'] = secondary_brand_id
        sneaker['silhouette_id'] = silhouette_id
        
    else:
        
        sneaker_values = sneaker_soup.find_all('div', class_='sd-brand-info__value')
        sneaker_values = list(map(textify, sneaker_values))
        sneaker_values = list(map(stripify, sneaker_values))
        
        sneaker = {key: np.nan for key in sneaker_keys} 
        sneaker['brand_id'] = brand_id
        sneaker['secondary_brand_id'] = secondary_brand_id
        sneaker['silhouette_id'] = silhouette_id
        sneaker['release_date_pretty'] = sneaker_values[0]
        sneaker['style_code'] = sneaker_values[1]
        sneaker['name'] = sneaker_values[2]
        sneaker['original_price_pretty'] = sneaker_values[3]
        
    if no_additional_data == False:
        sneaker_json.append(sneaker)
        brand_json.append(brand)
        secondary_brand_json.append(secondary_brand)
        silhouette_json.append(silhouette)
        
    else:
        sneaker_json.append(sneaker)

# get current month source page
current_url = urls

try:
    source = requests.get(current_url, time.sleep(3)).text
except:
    pass

source_soup = BeautifulSoup(source, features="html.parser")
monthly_sneakers = source_soup.find_all('div', class_='col-xs-12 col-sm-6') 

# loop over sneaker source page
for index, sneaker in enumerate(monthly_sneakers):
    if index % 2:
        continue

    sneaker_url = solecollector_com + monthly_sneakers[index].a['href']
    sneaker_html = requests.get(sneaker_url).text
    sneaker_soup = BeautifulSoup(sneaker_html, features="html.parser")

    try:
        sneaker_script = str(sneaker_soup.find_all('script', type="text/javascript")[2])
    except IndexError:
        break
    get_data(sneaker_soup, sneaker_script)   

# directory to save data
cur_dir = os.getcwd()
data = Path(cur_dir)
data = data / "data" / "01_raw"/ "update"

# save data
sneaker_df = pd.DataFrame(sneaker_json)
sneaker_df = sneaker_df.sort_values(by='release_date', ascending=False)
sneaker_df = sneaker_df.drop_duplicates(subset=['id'])
sneaker_df = sneaker_df.drop_duplicates(subset=['style_code'])
sneaker_df.to_csv(data / 'sneaker.csv', index=False)

brand_df = pd.DataFrame(brand_json)
brand_df = brand_df.sort_values(by='id', ascending=True)
brand_df = brand_df.drop_duplicates(subset=['id'])
brand_df.to_csv(data / 'brand.csv', index=False)

secondary_brand_df = pd.DataFrame(secondary_brand_json)
secondary_brand_df = secondary_brand_df.sort_values(by='id', ascending=True)
secondary_brand_df = secondary_brand_df.drop_duplicates(subset=['id'])
secondary_brand_df.to_csv(data / 'secondary_brand.csv', index=False)

silhouette_df = pd.DataFrame(silhouette_json)
silhouette_df = silhouette_df.sort_values(by='id', ascending=True)
silhouette_df = silhouette_df.drop_duplicates(subset=['id'])
silhouette_df.to_csv(data / 'silhouette.csv', index=False)