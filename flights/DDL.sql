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
