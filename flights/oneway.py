import http.client
from numpy import int64
import psycopg2
import pandas as pd
from dataload import create_connection,load_data,trunc_table    
from apiheaders import api_headers
import json

con = create_connection()
query="select a.country_code as in_code, a.airport_code as in_airport, b.country_code as nl_code, b.airport_code as nl_airport \
    from (select *,\'1\' as dummy from airport where country_code = \'IN\')a full outer join \
    (select *,\'1\' as dummy from airport where country_code = \'NL\')b on a.dummy = b.dummy"

in_nl_df = pd.read_sql_query(query, con=con)
#print(in_nl_df.head())
#in_nl_df = in_nl_df[in_nl_df['in_airport'] == "MAA"]
in_intl_air = ['MAA','DEL','BOM']#,'BLR','HYD','CCU']
in_nl_df=in_nl_df[in_nl_df['in_airport'].isin(in_intl_air)]


in_airport=set(list(in_nl_df['in_airport']))
nl_airport=set(list(in_nl_df['nl_airport']))
#print(nl_airport)

conn = http.client.HTTPSConnection("skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")
headers = api_headers()

table_name="quotes"
page_size =1000

con = create_connection()
trunc_table(con,table_name)


for in_air in in_airport:
    for nl_air in nl_airport:
        source=in_air+"-sky"
        dest=nl_air+"-sky"
        url="/apiservices/browseroutes/v1.0/IN/INR/en-US/%s/%s/anytime?inboundpartialdate=anytime" %(source,dest)

        print(url)
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str=data.decode("utf-8")
        data_json=json.loads(data_str)
        #quotes = data_json['Quotes']
        #print(data_json)
        if not 'errors' in data_json :
            if len(data_json['Quotes']) != 0 :
                quotes_df = pd.json_normalize(data_json['Quotes'])
                currency_df = pd.json_normalize(data_json['Currencies'])
                carriers_df = pd.json_normalize(data_json['Carriers'])
                places_df = pd.json_normalize(data_json['Places'])
        #print(df.info())

                if not quotes_df.empty:
                    quotes_df.columns = ['quote_id','min_price','is_direct','quote_datetime','carrier_id',\
                    'origin_id','destination_id','departure_date']
                    quotes_df['carrier_id'] = quotes_df['carrier_id'].explode().astype(int64)
                    currency = currency_df.rename(columns={'Code':'currency_code'})
                    currency = pd.DataFrame(currency)
                    currency = currency['currency_code']
                    carriers_df.columns = ['carrier_id','carrier_name']
                    places_df.columns = ['name','type','place_id','iata_code','skyscanner_code','city_name','city_id','country_name']
                    places_df= places_df[['place_id','iata_code','city_name','country_name']]
                    #print(places_df)
                    #print(quotes_df)

                    quotes_curr = quotes_df.merge(currency,how="cross")
                    quotes_curr_carrier = quotes_curr.merge(carriers_df, on='carrier_id',how='left')
                    qot_cur_car_origin = quotes_curr_carrier.merge(places_df, left_on='origin_id',right_on='place_id', how='left')
                    qot_cur_car_origin = qot_cur_car_origin.rename(columns={'iata_code':'origin_airport_code','city_name':'origin_city','country_name':'origin_country'})
                    qot_cur_car_org_dest = qot_cur_car_origin.merge(places_df,left_on='destination_id',right_on='place_id', how='left')
                    qot_cur_car_org_dest = qot_cur_car_org_dest.rename(columns={'iata_code':'dest_airport_code','city_name':'dest_city','country_name':'dest_country'})
                    qot_cur_car_org_dest = qot_cur_car_org_dest.drop(['place_id_x','place_id_y'],axis=1)
                    qot_cur_car_org_dest = qot_cur_car_org_dest[['quote_id','quote_datetime','departure_date','origin_city','origin_id','origin_airport_code','origin_country','dest_city','destination_id','dest_airport_code','dest_country','min_price','currency_code','is_direct','carrier_id','carrier_name']]
                    qot_cur_car_org_dest['quote_datetime'] =pd.to_datetime(qot_cur_car_org_dest['quote_datetime'])
                    qot_cur_car_org_dest['departure_date'] =pd.to_datetime(qot_cur_car_org_dest['departure_date'])
            
                #print(qot_cur_car_org_dest)

                    ## Check connection and load data:
            
                    if con == "":
                        print("Issue with connection")
                    else:
                    #trunc_table(con,table_name)
                        load_data(con,qot_cur_car_org_dest,table_name,page_size)

            


            


        
