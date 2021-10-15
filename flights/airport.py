import os
import pandas as pd
import json
import urllib.request as request
from dataload import create_connection,load_data,trunc_table


url ="http://api.travelpayouts.com/data/en/cities.json"

with request.urlopen(url) as response:
    if response.getcode() == 200:
        source = response.read()
        data = json.loads(source)
    else:
        print("Error when retrieving data")

#print(data)
df = pd.json_normalize(data)
df = df.iloc[:,:6]
df.columns = ['country_code','airport_code','airport_city','timezone','latitude','longitude']
#print(df.info())
df['airport_city'] = df['airport_city'].str.upper()

con = create_connection()

table_name="AIRPORT"
page_size =500
#print(con)

if con == "":
    print("Issue with connection")
else :
    trunc_table(con,table_name)
    load_data(con,df,table_name,page_size)
