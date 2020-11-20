# import packages
import pandas as pd
import os
from pathlib import Path
import numpy as np

# create path
update = Path(os.getcwd()) / '..' / '..'/ 'data' / '01_raw' / 'update'
sneaker = pd.read_csv(update / 'sneaker.csv')

# select data
sneaker = sneaker[['style_code', 'name', 'release_date', 'original_price', 'description','brand_id']]
sneaker = sneaker.rename(columns={'original_price':'retail_price', 'release_date':'date'})

# engineer features
sneaker['date'] = pd.to_datetime(sneaker['date'])
sneaker['release_month'] = sneaker['date'].dt.month
sneaker['release_dow'] = sneaker['date'].dt.weekday
month = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
dow = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
sneaker['release_month'] = sneaker['release_month'].map(month)
sneaker['release_dow'] = sneaker['release_dow'].map(dow)
sneaker['date'] = sneaker['date'].dt.date

sneaker['retail_price'] = sneaker['retail_price'].fillna(np.mean(sneaker.retail_price))
sneaker['name_join'] = sneaker['name'].str.lower()
sneaker['wmns'] = sneaker['name_join'].str.contains(r' wmns')
sneaker['collab'] = sneaker['name_join'].str.contains(r' x ')
sneaker['retro'] = sneaker['name_join'].str.contains(r' retro| og')
sneaker['kids'] = sneaker['name_join'].str.contains(r' gs| kid| kids')

# join brand
brand = pd.read_csv(update / 'brand.csv')
brand['name'] = brand['name'].str.title()
brand['name'] = brand['name'].str.replace('Jordan', 'Air Jordan')
valid_brands = ['Nike', 'Air Jordan', 'Adidas', 'Jordan Brand', 'Reebok',
       'Other Brands', 'Converse', 'Puma', 'New Balance', 'Asics', 'Vans',
       'Nike Basketball', 'Nike Running']
brand['name'] = brand['name'].apply(lambda x: 'Other Brands' if x not in valid_brands else x)
brand = brand.rename(columns={'id':'brand_id', 'name':'brand'})
brand = brand[['brand_id', 'brand']]

# create final dataset to make predictions
sneaker = sneaker.merge(brand, how='left', on='brand_id')

# output final dataset as test.csv
inter_update = Path(os.getcwd()) / '..' / '..'/ 'data' / '02_intermediate'
sneaker.to_csv(inter_update / 'test.csv', index=False)

