# Module 1 Homework: Docker & SQL

Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?

    ***24.3.1***
    24.2.1
    23.3.1
    23.2.1


# Question 2. Understanding Docker networking and docker-compose

Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

    postgres:5433
    localhost:5432
    ***db:5432***
    postgres:5432
```

Prepare Postgres

Run Postgres and load data as shown in the videos We'll use the green taxi trips from October 2019:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz`

You will also need the dataset with zones:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv`

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether you want to use Jupyter or a python script.


# Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

    Up to 1 mile
    In between 1 (exclusive) and 3 miles (inclusive),
    In between 3 (exclusive) and 7 miles (inclusive),
    In between 7 (exclusive) and 10 miles (inclusive),
    Over 10 miles

```
select count(lpep_pickup_datetime) as count,
  from green
  where
     trip_distance > 1 and
     trip_distance <= 3;
┌────────┐
│ count  │
│ int64  │
├────────┤
│ 199013 │
└────────┘
```

D select count(lpep_pickup_datetime) as count,
  from green
  where
     trip_distance > 3 and
     trip_distance <= 7;
┌────────┐
│ count  │
│ int64  │
├────────┤
│ 109645 │
└────────┘
D select count(lpep_pickup_datetime) as count,
  from green
  where
     trip_distance > 7 and
     trip_distance <= 10;
┌───────┐
│ count │
│ int64 │
├───────┤
│ 27688 │
└───────┘
D select count(lpep_pickup_datetime) as count,
  from green
  where
     trip_distance > 10;
┌───────┐
│ count │
│ int64 │
├───────┤
│ 35202 │
└───────┘


Answers:

    104,802; 197,670; 110,612; 27,831; 35,281
    104,802; 198,924; 109,603; 27,678; 35,189
    104,793; 201,407; 110,612; 27,831; 35,281
    104,793; 202,661; 109,603; 27,678; 35,189
    ***104,838; 199,013; 109,645; 27,688; 35,202***


# Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

select lpep_pickup_datetime, max(trip_distance)
  from green
  where lpep_pickup_datetime in ('2019-10-11','2019-10-24', '2019-10-26', '2019-10-31')
  group by lpep_pickup_datetime;

┌──────────────────────┬────────────────────┐
│ lpep_pickup_datetime │ max(trip_distance) │
│      timestamp       │       double       │
├──────────────────────┼────────────────────┤
│ 2019-10-11 00:00:00  │              18.03 │
│ 2019-10-31 00:00:00  │              10.52 │
└──────────────────────┴────────────────────┘

Tip: For every day, we only care about one single trip with the longest distance.

    ***2019-10-11***
    2019-10-24
    2019-10-26
    2019-10-31


# Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?


create table green as select * from read_csv_auto('data/green_tripdata_2019-10.csv');
create table zones as select * from read_csv_auto('data/taxi_zone_lookup.csv');

PRAGMA table_info(green);
PRAGMA table_info(zones);

# This isn't finished

select count(PULocationID), Zone from green join zones on PULocationID = LocationID
‣ group by PULocationID, "Zone"
· order by count(PULocationID) desc;



Consider only lpep_pickup_datetime when filtering by date.

    East Harlem North, East Harlem South, Morningside Heights
    East Harlem North, Morningside Heights
    Morningside Heights, Astoria Park, East Harlem South
    Bedford, East Harlem North, Astoria Park


# Question 6. Largest tip

For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's tip , not trip
We need the name of the zone, not the ID.

```
SELECT
      green.lpep_pickup_datetime,
      green.trip_distance,
      green.fare_amount,
      green.tip_amount,
      dropoff_zones.Zone
  FROM
      green
  JOIN
      zones AS pickup_zones ON green.PULocationID = pickup_zones.LocationID
  JOIN
      zones AS dropoff_zones ON green.DOLocationID = dropoff_zones.LocationID
  WHERE
      pickup_zones.Zone = 'East Harlem North'
      AND MONTH(green.lpep_pickup_datetime) = 10
      AND YEAR(green.lpep_pickup_datetime) = 2019
  ORDER BY
      green.tip_amount DESC
  LIMIT 10;
┌──────────────────────┬───────────────┬─────────────┬────────────┬───────────────────────┐
│ lpep_pickup_datetime │ trip_distance │ fare_amount │ tip_amount │         Zone          │
│      timestamp       │    double     │   double    │   double   │        varchar        │
├──────────────────────┼───────────────┼─────────────┼────────────┼───────────────────────┤
│ 2019-10-25 15:50:05  │         17.01 │        52.0 │       87.3 │ JFK Airport           │
│ 2019-10-28 06:05:56  │          1.45 │         6.0 │      80.88 │ Yorkville West        │
│ 2019-10-24 14:35:52  │          0.02 │         2.5 │       40.0 │ East Harlem North     │
│ 2019-10-01 00:42:36  │           0.0 │         2.5 │       35.0 │ East Harlem North     │
│ 2019-10-20 15:14:27  │         26.61 │        93.0 │      26.45 │ Newark Airport        │
│ 2019-10-11 07:22:48  │          17.2 │        47.5 │       20.0 │ JFK Airport           │
│ 2019-10-31 13:51:23  │          2.48 │        18.0 │      18.45 │ Upper East Side North │
│ 2019-10-14 09:44:20  │         17.11 │        52.0 │      17.68 │ JFK Airport           │
│ 2019-10-19 16:55:24  │          16.8 │        52.0 │      17.68 │ JFK Airport           │
│ 2019-10-19 13:19:46  │          17.9 │        52.0 │      17.65 │ JFK Airport           │
├──────────────────────┴───────────────┴─────────────┴────────────┴───────────────────────┤
│ 10 rows                                                                       5 columns │
└─────────────────────────────────────────────────────────────────────────────────
```


    Yorkville West
    ***JFK Airport***
    East Harlem North
    East Harlem South

Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. Copy the files from the course repo here to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


# Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

    Downloading the provider plugins and setting up backend,
    Generating proposed changes and auto-executing the plan
    Remove all resources managed by terraform`

Answers:

    terraform import, terraform apply -y, terraform destroy
    teraform init, terraform plan -auto-apply, terraform rm
    terraform init, terraform run -auto-approve, terraform destroy
    terraform init, terraform apply -auto-approve, terraform destroy
    terraform import, terraform apply -y, terraform rm

