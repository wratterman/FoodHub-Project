# FoodHub-Project

## Usage

### Prerequisites to be Installed

- PostgreSQL [Click Here to Download Postgres](https://www.postgresql.org/download/)
- Python3+ [Click Here to Download Python](https://www.python.org/downloads/)
- Pip3+ [Click Here to Download Pip](https://pip.pypa.io/en/stable/cli/pip_install/)

or

- Docker [Click Here to Docker](https://docs.docker.com/engine/install/)
- docker-compose [Click Here to Compose](https://docs.docker.com/compose/install/)

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
# OR
$ pip install psycopg2-binary
$ pip install pandas
$ pip install pprintpp
$ python run_migrations.py
```

**Migration does the following**:

- Creates The following tables with foreign key relations
    - Restaurants
    - Cuisines
    - Restaurant Cuisines (Joins Table)
    - Menus 
    - Restaurant Menus  (Joins Table)
    - Items
    - Restaurant Menu Items (Joins Table)
    - Logo Photos 
    - Restaurant Logos (Joins Table)
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

### Verify in Postgres

Open Postgres from the terminal using `psql` and then:

```sql
\x auto; -- Turns on Auto Extended Display

-- tables
\dt; -- view all tables
SELECT * FROM restaurants;
SELECT * FROM cuisines;
SELECT * FROM menus;
SELECT * FROM items;
SELECT * FROM logo_photos;
SELECT * FROM restaurant_cuisines;
SELECT * FROM restaurant_logos;
SELECT * FROM restaurant_menus;
SELECT * FROM restaurant_menu_items;

-- functions
\df; -- view all functions
SELECT * FROM menu_items_by_cuisine_and_price('Mediterranean', 15);
SELECT * FROM menu_items_by_cuisine_and_price('American', 15);
-- Generage Random Cuisine to provide for function
SELECT * FROM menu_items_by_cuisine_and_price(
    (
        SELECT 
            name 
        FROM cuisines 
        ORDER BY random() 
        LIMIT 1
    ), 
    15)
;

-- Playground
-- Search for Items under $10 on Dessert Menus
SELECT 
    r.restaurant_id AS restaurant_id, 
    r.name AS restaurant, 
    c.name AS cuisine, 
    m.category_name AS menu, 
    i.product_id AS item_id, 
    i.name AS item, 
    i.price AS price 
FROM restaurants r 
INNER JOIN restaurant_cuisines rc 
    ON r.id = rc.restaurant_id 
INNER JOIN cuisines c 
    ON rc.cuisine_id = c.id 
INNER JOIN restaurant_menu_items rmi 
    ON r.id = rmi.restaurant_id 
INNER JOIN menus m 
    ON rmi.menu_id = m.id 
INNER JOIN items i 
    ON rmi.item_id = i.id 
WHERE m.category_name ILIKE '%dessert%' -- Any menu category_name
    AND i.price < 10 -- Any desired max_price
ORDER BY restaurant, restaurant_id, price;

-- Average Item Price by Cuisine Type
SELECT
    c.name as cuisine,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine
ORDER BY avg_item_price;

-- Average Item Price by Cuisine + Menu Type
SELECT
    c.name as cuisine,
    m.category_name as menu,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN menus m
    ON rmi.menu_id = m.id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine, menu
ORDER BY cuisine, avg_item_price;

-- Average Item Price by Cuisine + Menu Type With Overall Cuisine Average across Menus
SELECT
    c.name as cuisine,
    'ALL MENUS' as menu,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine

UNION

SELECT
    c.name as cuisine,
    m.category_name as menu,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN menus m
    ON rmi.menu_id = m.id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine, menu
ORDER BY cuisine, avg_item_price;

```
