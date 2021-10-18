import http.client
from typing import Collection
from numpy import int64
import psycopg2
import pandas as pd
from dataload import create_connection,load_data,trunc_table    
from apiheaders import api_headers
import json

##Create DB connection to get the retrieve the aiports/cities to check for prices. 
con = create_connection()
query="select a.country_code as in_code, a.airport_code as in_airport, b.country_code as nl_code, b.airport_code as nl_airport \
    from (select *,\'1\' as dummy from airport where country_code = \'IN\')a full outer join \
    (select *,\'1\' as dummy from airport where country_code = \'NL\')b on a.dummy = b.dummy"

in_nl_df = pd.read_sql_query(query, con=con)
in_intl_air = ['MAA','DEL','BOM']#,'BLR','HYD','CCU']
in_nl_df=in_nl_df[in_nl_df['in_airport'].isin(in_intl_air)]

in_airport=set(list(in_nl_df['in_airport']))
nl_airport=set(list(in_nl_df['nl_airport']))

##Create connection to read data from the api
conn = http.client.HTTPSConnection("skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")
headers = api_headers()

table_name="roundtrip_quotes"
page_size =100

## create db connection to truncate the table for re-runs
con = create_connection()
trunc_table(con,table_name)

## start to get the locations:
for in_air in in_airport:
    for nl_air in nl_airport:
        source=in_air+"-sky"
        dest=nl_air+"-sky"
        url = "/apiservices/browsequotes/v1.0/IN/INR/en-US/%s/%s/anytime/anytime" %(source,dest)
        print(url)

        conn.request("GET", url , headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str = data.decode("utf-8")
        data_json = json.loads(data_str)

        ##check if we have valid output from the api:
        if not 'errors' in data_json :
            if len(data_json['Quotes']) != 0 :
                quotes_df = pd.json_normalize(data_json['Quotes'])
                currency_df = pd.json_normalize(data_json['Currencies'])
                carriers_df = pd.json_normalize(data_json['Carriers'])
                places_df = pd.json_normalize(data_json['Places'])
            
                ##Check if the quotes data is not empty to process the required fields. 
                if not quotes_df.empty:
                    quotes_df.columns = ['quote_id','min_price','is_direct','quote_datetime',
                     'out_carrier_id','out_origin_id','out_destination_id','out_departure_date',
                     'in_carrier_id','in_origin_id','in_destination_id','in_departure_date',
                     ]
                    quotes_df['out_carrier_id'] = quotes_df['out_carrier_id'].explode().astype(int64)
                    quotes_df['in_carrier_id'] = quotes_df['in_carrier_id'].explode().astype(int64)
                    #print(quotes_df.T)
                    currency = currency_df.rename(columns={'Code':'currency_code'})
                    currency = pd.DataFrame(currency)['currency_code']
                    carriers_df.columns = ['carrier_id','carrier_name']
                    places_df.columns = ['name','type','place_id','iata_code','skyscanner_code','city_name','city_id','country_name']
                    places_df= places_df[['place_id','iata_code','city_name','country_name']]

                    quotes_curr = quotes_df.merge(currency,how="cross")
                    quotes_cur_carrier_out = quotes_curr.merge(carriers_df, left_on="out_carrier_id", right_on="carrier_id", how='left')
                    quotes_cur_carrier = quotes_cur_carrier_out.merge(carriers_df, left_on="in_carrier_id", right_on="carrier_id", how='left')
                    quotes_cur_carrier = quotes_cur_carrier.drop(['carrier_id_x','carrier_id_y'], axis = 1)
                    quotes_cur_carrier = quotes_cur_carrier.rename(columns={'carrier_name_x':'out_carrier_name','carrier_name_y':'in_carrier_name'})
                    
                    quotes_cur_carrier.insert(15,'out_origin_city_name',quotes_cur_carrier['out_origin_id'].map(places_df.set_index('place_id')['city_name']))
                    quotes_cur_carrier.insert(16,'out_origin_city_code',quotes_cur_carrier['out_origin_id'].map(places_df.set_index('place_id')['iata_code']))
                    quotes_cur_carrier.insert(17,'out_origin_country_code',quotes_cur_carrier['out_origin_id'].map(places_df.set_index('place_id')['country_name']))

                    quotes_cur_carrier.insert(18,'out_dest_city_name',quotes_cur_carrier['out_destination_id'].map(places_df.set_index('place_id')['city_name']))
                    quotes_cur_carrier.insert(19,'out_dest_city_code',quotes_cur_carrier['out_destination_id'].map(places_df.set_index('place_id')['iata_code']))
                    quotes_cur_carrier.insert(20,'out_dest_country_code',quotes_cur_carrier['out_destination_id'].map(places_df.set_index('place_id')['country_name']))

                    quotes_cur_carrier.insert(21,'in_orig_city_name',quotes_cur_carrier['in_origin_id'].map(places_df.set_index('place_id')['city_name']))
                    quotes_cur_carrier.insert(22,'in_orig_city_code',quotes_cur_carrier['in_origin_id'].map(places_df.set_index('place_id')['iata_code']))
                    quotes_cur_carrier.insert(23,'in_orig_country_code',quotes_cur_carrier['in_origin_id'].map(places_df.set_index('place_id')['country_name']))

                    quotes_cur_carrier.insert(24,'in_dest_city_name',quotes_cur_carrier['in_destination_id'].map(places_df.set_index('place_id')['city_name']))
                    quotes_cur_carrier.insert(25,'in_dest_city_code',quotes_cur_carrier['in_destination_id'].map(places_df.set_index('place_id')['iata_code']))
                    quotes_cur_carrier.insert(26,'in_dest_country_code',quotes_cur_carrier['in_destination_id'].map(places_df.set_index('place_id')['country_name']))

                    quotes_cur_carrier['quote_datetime'] = pd.to_datetime(quotes_cur_carrier['quote_datetime'])
                    quotes_cur_carrier['out_departure_date'] = pd.to_datetime(quotes_cur_carrier['out_departure_date'])
                    quotes_cur_carrier['in_departure_date'] = pd.to_datetime(quotes_cur_carrier['in_departure_date'])

                    quotes_cur_carrier = quotes_cur_carrier[['quote_id','is_direct','min_price','currency_code','quote_datetime','in_carrier_id','in_carrier_name','in_departure_date',
                                                             'in_origin_id','in_orig_city_name','in_orig_city_code','in_orig_country_code','in_destination_id','in_dest_city_name','in_dest_city_code','in_dest_country_code',
                                                             'out_carrier_id','out_carrier_name','out_departure_date','out_origin_id','out_origin_city_name','out_origin_city_code','out_origin_country_code',
                                                             'out_destination_id','out_dest_city_name','out_dest_city_code','out_dest_country_code']]
                    #print(quotes_cur_carrier.info())
                    if con == "":
                        print("Issue with connection")
                    else:
                        load_data(con,quotes_cur_carrier,table_name,page_size)


