# FoodHub-Project

## Usage

### Prerequisites to be Installed

- PostgreSQL
- Python3+
- Pip3+

or

- Docker
- docker-compose

## If Using Docker (Recommended)

```shell
$ rm output_csvs/**/*.csv 
# Removes all Csvs inside the output_csvs directory and subdirs
$ docker-compose run -v $(pwd)/output_csvs:/app/output_csvs python-app
```

This will execute a build + run of a PG DB image with persistent storage as well as execute the script and write out the output files to the `output_csvs/` directory on your local machine. You should see printed log statements showing you when the process has completed and output files have been written, and those files should be visible on you local machine.

Similarly, the DB image can be queried by running the following:

```shell
$ docker exec -it foodhub-project-db-1 psql -d pg_development -U postgres
```

This will open up the PSQL session inside your terminal and you can execute a number of queries similar to if you were querying a locally provisioned DB. Sample Queries can be found at the bottom of the README


## If running locally

### Set local values for config file configuring local PG

***THIS IS NOT NEEDED IF YOU USE DOCKER***

If you haven't already, download Postgres to your machine and export your the DB_Name, DB_USERNAME, and DB_PASSWORD to system variables

```shell
$ createdb your-db-name
$ export DB_NAME=your-db-name
$ export DB_USERNAME=your-db-username
$ export DB_PASSWORD=your-db-password
```

### Setup to Install Deps + Run Migrations

```shell
$ pip install -r requirements.txt
$ python run_migrations.py
```

**Migration does the following**:

- Creates The following tables with foreign key relations
    - Restaurants
    - Cuisines
    - Restaurant Cuisines (Joins Table)
    - Menus (Belongs to Restaurant)
    - Items
    - Menu Items (Joins Table)
    - Logo Photos (Belongs to Restaurant)
- Creates the following Function:
    - menu_items_by_cuisine_and_price(cuisine_type, max_price)
        - Returns a list of items from menus at restaurants that match the provided cuisine type at a price equal to or below the maximum provided
        - **Defaults to 'Mediterranean' and 15**

### Schema Diagram

<img width="1376" alt="FoodHub-schema-diagram" src="https://github.com/wratterman/FoodHub-Project/assets/25143074/430d4e4c-c0b4-45ca-b8b4-f85e62ab9b80">

### Execute the Loader

```shell
$ python main.py
```

**What this does:**

- Loads in data from the `FoodHub_data.json` found in the `input_data/` directory with special character handling
    - Iterates over list of restaurants and creates restaurants
    - Then using the restaurant_id, it goes on to create children objects (menus, logo_photos) as well as many-to-many relations like Restaurant-Cuisines and late menu-items
    - Logic for this can primarily be found in `data_orchestrator/data_loader.py` with actual DB insert statements found in `db/db_utils.py`
- In `data_orchestrator/data_exporter.py`
    - Writes out data from provisioned tables into `output_csvs/` directory with filenames that match the source table name
    - Executes `menu_items_by_cuisine_and_price(cuisine_type, max_price)` for ever listed Cuisine Type and a default max price of $15.
        - Writes out the results to `output_csvs/query_results/` then with the file name matching the following pattern: `{CUISINE_TYPE}_items_below_15_dollars.csv` 

### Verify in Postgres (with 100 limits)

Open Postgres from the terminal using `psql` and then:

```sql
\x on; -- Turns on Extended Display

-- tables
\dt; -- view all tables
SELECT * FROM restaurants LIMIT 100;
SELECT * FROM cuisines LIMIT 100;
SELECT * FROM menus LIMIT 100;
SELECT * FROM items LIMIT 100;
SELECT * FROM logo_photos LIMIT 100;
SELECT * FROM restaurant_cuisines LIMIT 100;
SELECT * FROM menu_items LIMIT 100;

-- functions
\df; -- view all functions
SELECT * FROM menu_items_by_cuisine_and_price('Mediterranean', 15) LIMIT 100;
SELECT * FROM menu_items_by_cuisine_and_price('American', 15) LIMIT 100;

```
