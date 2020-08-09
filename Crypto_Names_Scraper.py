# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 00:55:26 2020

Script that get the names of all cryptocurrencies included into the 
coinmarketcap website. 

@author: mariano
"""

#---------------------------------
# 0. Import packages
#---------------------------------
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
import settings


#---------------------------------------------
# 1. Extract all ids of al cryptocurrencies
#---------------------------------------------

# 1.1  Define templates to store values 
slug        = []
rank        = []
code          = []
marketcap   = []

# 1.2 Define list to access all coinmarketcap pages 
pages = list(range(1, 29))

# 1.3 Loop through all coinmarketcap pages
for p in pages:

# 1.3.0 Control de looping
   print("Scrapping page: " , p )

# 1.3.1 Pause loop to avoid error 429
   time.sleep( 1 )

# 1.3.2 Scrape website p using beautifulSoup library
   url = 'https://coinmarketcap.com/%s/' % (p)
   cmc = requests.get(url)
   soup = BeautifulSoup(cmc.content,'html.parser')

# 1.3.3 Localize the information in the scrapped soup object
   data = soup.find('script', id="__NEXT_DATA__",type="application/json")

# 1.3.4 Generate a dictionary
   coins = {}

# 1.3.5 Load the info obtained as json 
   coin_data = json.loads(data.contents[0])

# 1.3.6 Generate a list from the coins info 
   listing = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

# 1.3.7 Add coins dictionary elements to each template list
   for i in listing:
     slug.append(i['slug'])
     rank.append(i['rank'])
     code.append(i['id'])
     marketcap.append(i['quote']['USD']['market_cap'])


print("")
print("Scrapping names completed\n")

#---------------------------------------------
# 2. Store data 
#---------------------------------------------
print("Save names into directory \n") 

# 2.1 Create dataframe
df = pd.DataFrame(columns=['slug','rank','id','marketcap'])

# 2.2 Fill dataframe with information
df['slug']        = slug
df['rank']        = rank
df['id']          = code
df['marketcap']   = marketcap

# 2.3 Save all coins information in local drive

# 2.3.1 Get user name defined in settings
User_Name = settings.User_Name

# 2.3.2 Save the file 
df.to_csv("C:/Users/{}/Crypto_Scraper/Data/Coin_Names.csv".format(User_Name),index = False, header=True)