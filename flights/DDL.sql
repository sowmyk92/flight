--CURRENCY TABLE 
DROP TABLE CURRENCY ;
create table CURRENCY
(
    CODE char(3) ,
	symbol varchar(10),
	thousand_separator varchar(10),  
	decimal_separator  varchar(10),
	symbol_on_left    boolean,
	space_amt_symbol  boolean,
	round_coefficient int,
	decimal_digits    int
);
####################################################################################################################################################################################
--COUNTRY TABLE 
DROP TABLE COUNTRY;
CREATE TABLE COUNTRY
(
	COUNTRY_CODE VARCHAR(10),
	COUNTRY_NAME VARCHAR(100),
	CURRENCY_CODE CHAR(3)
);
####################################################################################################################################################################################
--AIRPORT TABLE 
DROP TABLE AIRPORT;
CREATE TABLE AIRPORT
(
	COUNTRY_CODE VARCHAR(100),
	AIRPORT_CODE VARCHAR(10),
	AIRPORT_CITY VARCHAR(100),
	LATITUDE DECIMAL(8,6),
	LONGITUDE DECIMAL(9,6),
	TIMEZONE TEXT
);
####################################################################################################################################################################################
--QUOTES TABLE 
DROP table ONEWAY_QUOTES;
create table ONEWAY_QUOTES
(
	quote_id  int,
	quote_datetime timestamp,
	departure_date timestamp,
	origin_city varchar(100),
	origin_id int,
	origin_airport_code varchar(100),
	origin_country varchar(100),
	dest_city varchar(100),
	destination_id int,
	dest_airport_code varchar(100),
	dest_country varchar(100),
	min_price decimal(28),
	currency_code char(3),
	is_direct boolean,
	carrier_id int,
	carrier_name varchar(100)
);
####################################################################################################################################################################################
--ROUNDTRIP QUOTES
DROP TABLE ROUNDTRIP_QUOTES;
CREATE TABLE ROUNDTRIP_QUOTES
(
	quote_id  int,
	is_direct boolean,
	min_price decimal(28),
	currency_code char(3),
	quote_datetime timestamp,
	in_carrier_id int,
	in_carrier_name varchar(100),
	in_departure_date timestamp, 
	in_origin_id int, 
	in_orig_city_name varchar(100),
	in_orig_city_code varchar(100),
	in_orig_country_code varchar(100),
	in_destination_id int,
	in_dest_city_name varchar(100), 
	in_dest_city_code varchar(100),
	in_dest_country_code varchar(100),
	out_carrier_id int, 
	out_carrier_name varchar(100),
	out_departure_date varchar(100),
	out_origin_id int,
	out_origin_city_name varchar(100),
	out_origin_city_code varchar(100),
	out_origin_country_code varchar(100),
	out_destination_id int, 
	out_dest_city_name varchar(100), 
	out_dest_city_code varchar(100),
	out_dest_country_code  varchar(100)
);
####################################################################################################################################################################################