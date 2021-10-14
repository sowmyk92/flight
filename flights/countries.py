import os
import http.client
import json
import pandas as pd
import sql
import psycopg2
from dataload import create_connection,load_data,trunc_table
from apiheaders import api_headers

## Connect to the API to fetch data
conn = http.client.HTTPSConnection("skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")

headers =  api_headers()
url= "/apiservices/reference/v1.0/countries/en-US"
conn.request("GET",url,headers= headers)
#conn.request("GET", "/apiservices/reference/v1.0/countries/en-US", headers=headers)

res = conn.getresponse()
data= res.read()
data_Str = data.decode("utf-8")
data_json = json.loads(data_Str)

#print(data_json)
df = pd.json_normalize(data_json['Countries'])
df.columns=['country_code','country_name']

#print(df[df['country_name'].isna() == True])
table_name="COUNTRY"
page_size =300

con = create_connection()
if con == "":
    print("Issue with connection")
else :
    trunc_table(con,table_name)
    load_data(con,df,table_name,page_size)
