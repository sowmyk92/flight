import http.client
import json
import pandas as pd
import sql
import psycopg2
from dataload import create_connection,load_data,trunc_table

## Connect to the API to fetch data
conn = http.client.HTTPSConnection("skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")
headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "7692c74fc6mshf16a988f8f40fa2p1276fejsn99bbe640a15c"
    }

conn.request("GET", "/apiservices/reference/v1.0/currencies", headers=headers)
res = conn.getresponse()
data = res.read()
data_Str = data.decode("utf-8")
data_json = json.loads(data_Str)

## Convert data into dataframe
df = pd.json_normalize(data_json['Currencies'])
df.columns = ['code','symbol','thousand_separator','decimal_separator','symbol_on_left',
'space_amt_symbol','round_coefficient','decimal_digits']

## clean the empty data
df.thousand_separator.value_counts()
df['thousand_separator'] = df['thousand_separator'].str.replace(u'\xa0', u'NA')

## table details :
table_name="currency"
page_size =100

## Check connection and load data:
con = create_connection()
if con == "":
    print("Issue with connection")
else :
    trunc_table(con,table_name)
    load_data(con,df,table_name,page_size)

