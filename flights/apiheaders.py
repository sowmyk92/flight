import os

def api_headers():
    with open("apicred.txt",'r') as f:
        apicred = f.readlines()

    for line in apicred:
        val=line.replace("\n","").split("=")
        if 'host' in val :
            host = val[1]
        if 'apikey' in val:
            apikey=val[1]

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': apikey
            }

    return headers
