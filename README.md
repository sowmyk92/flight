# Aim : To read data from API and load into tables

### API : Skyscanner API to read flight details

### Scripts:
1. apiheaders.py --> To retrieve the API headers (host,key) used for connection 

2. dataload.py --> To open DB connection, truncate table (if needed) and load data into the necessary tables. 

3. country.py --> Contains COUNTRY_CODE,COUNTRY_NAME and CURRENCY_CODE for each country 

![image](https://user-images.githubusercontent.com/67071872/137535370-5f81a998-4539-4de8-a4cf-1d97dd94108f.png)


4. currency.py --> Contains currency related information. 

![image](https://user-images.githubusercontent.com/67071872/137535505-765f282d-379c-469f-9c7b-a96a41e9921c.png)

5. airport.py --> contains airport code, city, country_code, latitude, longitude and timezone for each airports

![image](https://user-images.githubusercontent.com/67071872/137535719-ad69fed4-aa34-4469-ae5a-22605e742d95.png)
