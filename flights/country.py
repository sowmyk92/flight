import os
import pandas as pd
import json
import urllib.request as request
from dataload import create_connection,load_data,trunc_table

url = "http://api.travelpayouts.com/data/en/countries.json"

with request.urlopen(url) as response:
    if response.getcode() == 200:
        source = response.read()
        data = json.loads(source)
    else:
        print("Error when retrieving data")

df = pd.json_normalize(data)
df = df[['code','name','currency']]
df.columns = ['country_code','country_name','currency_code']
df['country_name'] = df['country_name'].str.upper()
df['currency_code'] = df['currency_code'].replace('','NA')
#df['currency_code'] = df['currency_code'].str.startswith(' ')
#print(df.info())


table_name="COUNTRY"
page_size =300

con = create_connection()
if con == "":
    print("Issue with connection")
else :
    trunc_table(con,table_name)
    load_data(con,df,table_name,page_size)


