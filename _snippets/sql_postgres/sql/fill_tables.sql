-- Set params
set session my.number_of_sales = '2000';
set session my.number_of_users = '500';
set session my.number_of_products = '30';
set session my.number_of_stores = '5';
set session my.number_of_coutries = '5';
set session my.number_of_cities = '30';
set session my.status_names = '5';
set session my.start_date = '2019-01-01 00:00:00';
set session my.end_date = '2020-02-01 00:00:00';

-- load the pgcrypto extension to gen_random_uuid ()
CREATE EXTENSION pgcrypto;

-- Filling of products
INSERT INTO product
select id, concat('Product ', id) 
FROM GENERATE_SERIES(1, current_setting('my.number_of_products')::int) as id;

-- Filling of countries
INSERT INTO country
select id, concat('Country ', id) 
FROM GENERATE_SERIES(1, current_setting('my.number_of_coutries')::int) as id;

-- Filling of cities
INSERT INTO city
select id
	, concat('City ', id)
	, floor(random() * (current_setting('my.number_of_coutries')::int) + 1)::int
FROM GENERATE_SERIES(1, current_setting('my.number_of_cities')::int) as id;

-- Filling of stores
INSERT INTO store
select id
	, concat('Store ', id)
	, floor(random() * (current_setting('my.number_of_cities')::int) + 1)::int
FROM GENERATE_SERIES(1, current_setting('my.number_of_stores')::int) as id;

-- Filling of users
INSERT INTO users
select id
	, concat('User ', id)
FROM GENERATE_SERIES(1, current_setting('my.number_of_users')::int) as id;

-- Filling of users
INSERT INTO status_name
select status_name_id
	, concat('Status Name ', status_name_id)
FROM GENERATE_SERIES(1, current_setting('my.status_names')::int) as status_name_id;

-- Filling of sales  
INSERT INTO sale
select gen_random_uuid ()
	, round(CAST(float8 (random() * 10000) as numeric), 3)
	, TO_TIMESTAMP(start_date, 'YYYY-MM-DD HH24:MI:SS') +
		random()* (TO_TIMESTAMP(end_date, 'YYYY-MM-DD HH24:MI:SS') 
							- TO_TIMESTAMP(start_date, 'YYYY-MM-DD HH24:MI:SS'))
	, floor(random() * (current_setting('my.number_of_products')::int) + 1)::int
	, floor(random() * (current_setting('my.number_of_users')::int) + 1)::int
	, floor(random() * (current_setting('my.number_of_stores')::int) + 1)::int
FROM GENERATE_SERIES(1, current_setting('my.number_of_sales')::int) as id
	, current_setting('my.start_date') as start_date
	, current_setting('my.end_date') as end_date;

-- Filling of order_status  
INSERT INTO order_status
select gen_random_uuid ()
	, date_sale + random()* (date_sale + '5 days' - date_sale)
	, sale_id
	, floor(random() * (current_setting('my.status_names')::int) + 1)::int
from sale;


INSERT INTO Dim_Centres VALUES ('North', 'N01', 'Manta');
INSERT INTO Dim_Centres VALUES ('North', 'N02', 'Vaross');
INSERT INTO Dim_Centres VALUES ('East', 'E01', 'Mavaka');
INSERT INTO Dim_Centres VALUES ('East', 'E02', 'Bragow');
INSERT INTO Dim_Centres VALUES ('East', 'E03', 'Ralo');
INSERT INTO Dim_Centres VALUES ('South', 'S01', 'Verton');
INSERT INTO Dim_Centres VALUES ('South', 'S01', 'Cosa');
INSERT INTO Dim_Centres VALUES ('West', 'W01', 'Sleedburg');

INSERT INTO Map_Centre_Cust VALUES ('N01', 1);
INSERT INTO Map_Centre_Cust VALUES ('N01', 2);
INSERT INTO Map_Centre_Cust VALUES ('N02', 3);
INSERT INTO Map_Centre_Cust VALUES ('E01', 4);
INSERT INTO Map_Centre_Cust VALUES ('S01', 5);
INSERT INTO Map_Centre_Cust VALUES ('S02', 6);
INSERT INTO Map_Centre_Cust VALUES ('W01', 7);
INSERT INTO Map_Centre_Cust VALUES ('W01', 8);

INSERT INTO Fact_Centre_Txn VALUES ('N01', 1, '01/06/2017 09:00', 'N0100001', 100);
INSERT INTO Fact_Centre_Txn VALUES ('N01', 1, '01/06/2017 10:00', 'N0100002', 200);
INSERT INTO Fact_Centre_Txn VALUES ('N01', 1, '01/06/2017 14:30', 'N0100003', 175);
INSERT INTO Fact_Centre_Txn VALUES ('N01', 1, '02/06/2017 11:00', 'N0100005', 105);
INSERT INTO Fact_Centre_Txn VALUES ('S02', 6, '01/06/2017 10:30', 'S0200001', 90);
INSERT INTO Fact_Centre_Txn VALUES ('W01', 8, '03/06/2017 15:00', 'W0100001', 250);
