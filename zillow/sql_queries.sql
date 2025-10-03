USE economy;

/*
===============================================================================
Housing data script 
===============================================================================
Purpose:
    - Create view tables with housing data for utilization by the Power BI dashboard 
    - Provide two reports stating how a homebuyer can save the most money: 
		1) States after how many days on the market are house prices the most reduced 
        2) Which brokers have the highest drop in price compared to the original list price  

Highlights:
	1) Transformations (window functions, CASE statements etc.) were implemented on data from 
		the ETL pipeline to create a view with current housing market KPI data:
            - Average house price reduction per day, per city 
            - Percent of houses with reduced list price per day, per city 
            
	2) Found the average salary of job postings on ZipRecruiter per city, per day.
    3) Calculated historical (2016-2024) housing market KPIs from Realtor data.
    4) Segmented houses in price and days on market categories. 
    5) Found highest savings per segment categories. 
    6) Listed brokers with highest average drop in list price. 
===============================================================================
*/

CREATE OR REPLACE VIEW housing_data AS 
/*---------------------------------------------------------------------------
1) Transformation: add a column to flag the correct city based on the scraped 
	address column 
---------------------------------------------------------------------------*/
WITH city_transformation AS (
	SELECT 
		house_id,
		address, 
		price, 
		living_sqft, 
		days_on_zillow, 
		price_change, 
		date_extracted, 
		latitude, 
		longitude,
		CASE 
			WHEN address LIKE '%boise%' THEN 'boise'
			WHEN address LIKE '%harrisburg%' THEN 'harrisburg'
			ELSE 'grand rapids'
		END AS city
	FROM zillow_data
	WHERE date_extracted >= '2025-09-03'
), 
/*-----------------------------------------------------------------------------
2) Transformation: get the number of unique houses listed per day, and per city 
------------------------------------------------------------------------------*/
unique_houses AS (
	SELECT 
		date_extracted,
		city, 
		COUNT(DISTINCT house_id) AS total_distinct_houses
	FROM 
		city_transformation 
	GROUP BY 
		date_extracted,
		city
), 
/*---------------------------------------------------------------------------
3) Transformation: calculate the avg price reduction($) and percent of houses 
that have reduced their prices  
---------------------------------------------------------------------------*/
reduction_analytics AS (
	SELECT 
		ct.house_id,
		ct.city,
		ct.address, 
		ct.price, 
		ct.price_change,
		ROUND(AVG(ct.price_change) OVER(PARTITION BY ct.date_extracted, ct.city),2) AS avg_price_drop, 
		ROUND((
			COUNT(CASE WHEN ct.price_change < 0 THEN 1 END) OVER(PARTITION BY ct.date_extracted, ct.city) / 
			uh.total_distinct_houses
		),2) AS pct_reduced_houses,
		ct.latitude, 
		ct.longitude,
		ct.date_extracted 
	FROM 
		city_transformation ct
	JOIN 
		unique_houses uh ON ct.date_extracted = uh.date_extracted AND ct.city = uh.city
)
/*---------------------------------------------------------------------------
4) Combine: choose the data that will be displayed in the view 
---------------------------------------------------------------------------*/
SELECT 
	ra.house_id, 
	ra.city, 
	ra.address, 
	ra.price, 
	ra.price_change,
	ra.avg_price_drop,
	ra.pct_reduced_houses,
	ra.latitude, 
	ra.longitude,
	ra.date_extracted
FROM 
	reduction_analytics ra;
    
    SELECT * FROM housing_data;

/*----------------------------------------------------------------------------------
Calculate the avg salary per city and per day from ZIP job postings, store in a view 
------------------------------------------------------------------------------------*/
CREATE OR REPLACE VIEW city_salary AS 
  SELECT
	date_extracted,
	city,
	ROUND(SUM(salary * count) / SUM(count), 2) AS avg_salary
  FROM zip_salaries
  GROUP BY date_extracted, city;

/*--------------------------------------------------------------------------------------
Calculate historical KPIs: percent of houses with reduced prices, avg number of listings,
avg house price
---------------------------------------------------------------------------------------*/
CREATE OR REPLACE VIEW historical_data AS 
SELECT 
	`date`,
	city,
	ROUND(AVG(price_reduced_pct) OVER(PARTITION BY `date`, city), 2) AS avg_houses_reduced, 
	ROUND(AVG(total_listings) OVER(PARTITION BY `date`, city), 2) AS avg_listings, 
	ROUND(AVG(median_price) OVER(PARTITION BY `date`, city), 2) AS avg_price
FROM 
	realtor_historical_data;

/*--------------------------------------------------------------------------------------
House Segmentation: 
---------------------------------------------------------------------------------------*/
CREATE OR REPLACE VIEW segmented_data AS 
WITH city_data AS (
	SELECT 
		address, 
		broker,
		price,
		price_change,
		house_id,
		days_on_zillow,
		CASE 
			WHEN address LIKE '%boise%' THEN 'boise'
			WHEN address LIKE '%grand rapids%' THEN 'grand rapids'
			ELSE 'harrisburg'
		END AS city,
		date_extracted
	FROM zillow_data
	WHERE price_change IS NOT NULL AND broker IS NOT NULL
), prices_data AS (
	SELECT 
		broker,
		city,
		price,
		price_change,
		house_id,
		address,
		days_on_zillow,
		NTILE(3) OVER(PARTITION BY city ORDER BY price) AS price_rank,
		date_extracted
	FROM city_data
)
SELECT 
	broker,
	city,
	price,
	price_change,
	house_id,
	address,
	price_rank,
	days_on_zillow,
	NTILE(3) OVER(PARTITION BY city ORDER BY days_on_zillow) AS day_rank,
	date_extracted
FROM prices_data;

/*--------------------------------------------------------------------------------------
Find the avg price and avg price change per city based on how long the house has been 
on the market and its price
---------------------------------------------------------------------------------------*/
SELECT 
	city, 
	day_rank, 
	price_rank, 
	ROUND(AVG(price),2) AS avg_price, 
	ROUND(AVG(price_change),2) AS avg_price_change, 
	ROUND(AVG(days_on_zillow),2) AS avg_days
FROM 
	segmented_data 
GROUP BY 
	city, 
	price_rank, 
	day_rank
ORDER BY 
	avg_price_change;
	
/*--------------------------------------------------------------------------------------
Find the lowest avg price change per broker and city based on how long the house has been 
on the market and its price
---------------------------------------------------------------------------------------*/
WITH broker_stats AS (
	SELECT 
		broker,
		city,
		day_rank,
		price_rank,
		ROUND(AVG(price), 2) AS avg_price,
		ROUND(AVG(price_change), 2) AS avg_price_change,
		COUNT(DISTINCT house_id) AS unique_listings
	FROM 
		segmented_data
	GROUP BY 
		broker, 
		city, 
		day_rank, 
		price_rank
	HAVING 
		COUNT(DISTINCT house_id) >= 3
), ranked_brokers AS (
	SELECT 
		*,
		ROW_NUMBER() OVER (
			PARTITION BY city, day_rank, price_rank 
			ORDER BY avg_price_change ASC
		) AS rank_num
	FROM 
		broker_stats
)
SELECT 
	broker,
	city,
	day_rank,
	price_rank,
	avg_price,
	avg_price_change,
	unique_listings
FROM 
	ranked_brokers
WHERE 
	rank_num = 1
ORDER BY 
	day_rank, 
	price_rank;


