# -*- coding: utf-8 -*-
"""
- Script use the coinmarketcap api to extract information for all coins included into the 
coinmarketcap web. 
- The api is designed to extract information of just one coin in each api call. 
- In this script the calls are done in a loop for all the coins included into the previously
coin names cvs failed created by scrapping the coinmarketcap website. 

@author: mariano
"""

#-----------------------------------
# 0. Import packages
#-----------------------------------

import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import io
import time
import settings


#-----------------------------------
# 1. Load file with coin ids
#-----------------------------------

# 1.0  Get settings
User_Name = settings.User_Name
Api_Key = settings.Api_Key

# 1.1 Load the data from local drive
df = pd.read_csv("C:/Users/{}/Crypto_Scraper/Data/Coin_Names.csv".format(User_Name))


#-----------------------------------------------------------
# 2. Loop thorugh all coins and extract information
#-----------------------------------------------------------

# 2.1 Define template to store values 
slug        = []
i_d         = []
category    = []

# 2.2 Define api url to connect to
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

# 1.3 Use api key 
headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': Api_Key, 
}

# 1.4 Control iterations inside the loop
n = 0
count = 0

# 1.5 Loop through all coins id and extract the required information
for index, row in df.iterrows():
  
# 1.5.1 Get the id of current element in the loop
  i = row['id']

# 1.5.2 Pass the id as parameter to get information from using the api
  parameters = {
      'id': str(i)
   }

# 1.5.3 Call the api 
  session = Session()
  session.headers.update(headers)
  response = session.get(url, params=parameters)

# 1.5.4 Use the api as json object
  data = json.loads(response.text)

# 1.5.5 Pass information to the templates
  slug.append(data['data'][str(i)]['slug'])
  i_d.append(data['data'][str(i)]['id'])
  category.append(data['data'][str(i)]['category'])

# 1.5.6 Avoid over usage of the api 
  if n < 10:
    n = n + 1
    time.sleep( 1 )
  else: 
    n = 0
    time.sleep( 61 )

# 1.5.7 Display loop status
  count = count + 1
  print('-----------')
  print('Number of coins storage:', count)
  print('Current coin:', data['data'][str(i)]['slug'])
  print('')

print(' Api use completed \n')
#--------------------------------
# 1.6 Save information in cvs 
#--------------------------------

print(' Save information obtained \n')

# 1.6.1 Create dataframe
df_crypto = pd.DataFrame(columns=['slug','i_d','category'])

# 1.6.2 Fill dataframe with information
df_crypto['slug']        = slug
df_crypto['i_d']         = i_d
df_crypto['category']    = category

# 1.6.3 Save dataset in local drive
df.to_csv("C:/Users/{}/Crypto_Scraper/Data/Crypto_Info.csv".format(User_Name),index = False, header=True)