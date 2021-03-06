import os
import psycopg2
import json
import psycopg2.extras as extras


def connect_db(host,database,user,password):
    try:
        con = psycopg2.connect(dbname=database,user=user,password= password)
    
    except psycopg2.Error as e:
        print("Eror with connection: {}".format(e))

    return con

def create_connection():
    ''' To check the database connection  '''    
    with open("dbcred.txt","r") as f:
        param =f.readline()

    par = json.loads(param)
    for k,v in par.items():
        host = par['host']
        database = par['database']
        user = par['user']
        password = par['password']

    con = connect_db(host,database,user,password)
    return con

def load_data(con,df,table_name,page_size):
    ''' Function to load the dataframe to given table   '''    
    page_size= page_size

    ##Values for the insert command
    tp = [tuple(x) for x in df.to_numpy()]
    #print(tp)

    ##Colum names in order of the data for the insert query
    cols = ','.join(list(df.columns))
    print(cols)

    col1 =["%s" for x in df.columns]
    val = ','.join(col1)
    ##Construct the insert statement 
    query= "Insert into %s(%s) values(%s) " %(table_name, cols,val)
    print(query)

    cursor = con.cursor()
    try:
        v = extras.execute_batch(cursor,query,tp,page_size)
        print(v)
        con.commit()
    
    except(Exception,psycopg2.DatabaseError) as e:
        print("Error is :{}".format(e))
        con.rollback()
        con.close()
        
    print("Batch load completed")
    cursor.close()

def trunc_table(con,table_name):
    ''' Function to truncate the data of the given table   '''    
    query = "truncate table %s" %(table_name)
    print(query)
    cursor = con.cursor()
    try:
        cursor.execute(query)
        con.commit()
    
    except(Exception,psycopg2.DatabaseError) as e:
        print("Error is :{}".format(e))
        con.rollback()
        con.close()
            
    print("Truncate table : {} has been completed".format(table_name))
    cursor.close()    
