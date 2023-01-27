# Zoomcamp Homework

## Starting environment
You need to have docker and docker-compose v1-v2 on your machine.

#### <span style="color:cyan">Create .env file </span>
<code> $ touch .env </code>  


#### <span style="color:cyan">Set shown below env vars in .env file</span>
""""  
DATABASE_URL=postgresql://postgres:postgres@homework_db/homework1  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=postgres  
POSTGRES_DB=homework1
CHUNK_SIZE=Desired amount (INTEGER)
TAXI_CSV=green_tripdata_2019-01.csv
ZONE_CSV=taxi+_zone_lookup.csv
TAXI_LINK=http://your-ip:your-port/${TAXI_CSV}
ZONE_LINK=http://your-ip:your-port/${ZONE_CSV}

"""

Please, NOTE: I predownloaded csv files to my pc and downloaded to container via http.server, as shown in Video. If you want to download direct from source you need to unzip file. To do it change Dockerfile - install stage.


#### <span style="color:cyan">Start app containers with docker-compose.yml file</span>
<code> $ docker compose up --build </code>

## Homework Solutions
#### Note: Some questions have 2 solutions. They marked with V1 and V2 marks.

Question 3:  
<code>
SELECT date(lpep_pickup_datetime),
			 date(lpep_dropoff_datetime),
			 count(1)
  from green_taxi_data
 group by 1, 2
having date(lpep_pickup_datetime) = '2019-01-15'
   and date(lpep_dropoff_datetime) = '2019-01-15';
</code>  
Answer is 20530.

Question 4:  
<code>
V1:  
select DATE(lpep_pickup_datetime) as trip_day,
			 trip_distance
  from green_taxi_data
 order by trip_distance
  DESc limit 1;


V2:  
select date(lpep_pickup_datetime),
			 max(trip_distance)
  from green_taxi_data
 group by date(lpep_pickup_datetime)
 order by max(trip_distance)
  DESC limit 1;
</code>  
Answer is 2019-01-15 | 117.99

Question 5:  
<code>
V1:  
select date(lpep_dropoff_datetime),
		   date(lpep_pickup_datetime),
		   passenger_count,
			 count(1)
  from green_taxi_data
 where passenger_count in (2, 3)
   and date(lpep_pickup_datetime)  = date(lpep_dropoff_datetime)
   and date(lpep_pickup_datetime) = '2019-01-01'
 group by 1, 2, 3;
  
V2:  
select date(lpep_dropoff_datetime),
			 passenger_count,
			 count(1)
	from green_taxi_data
 where passenger_count in (2, 3)
   and date(lpep_pickup_datetime) = '2019-01-01'
 group by 1, 2
</code>  
Answer is 
2019-01-01 | 2               | 1282
2019-01-01 | 3               | 254

Question 6:  
<code>
SELECT zo."Zone"
  from zones zo
 where zo."LocationID" in (
			Select g."DOLocationID" as pickup_zone
			  from green_taxi_data g 
				join zones z on g."PULocationID"=z."LocationID"
			 where z."Zone" = 'Astoria'
			 order by tip_amount
        desc limit 1
);
</code>  
Answer is Long Island City/Queens Plaza