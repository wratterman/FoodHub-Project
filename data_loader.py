import csv

from db.db_utils import (
    insert_restaurants,
    insert_logo_photos,
    insert_cuisines,
    insert_menu,
    insert_items,
    insert_menu_items,
    insert_restaurant_cuisines,
)


def load_restaurant_data(data, cur):
    for restaurant_data in data["restaurants"]:
        insert_restaurants(cur, restaurant_data)
        restaurant_id = cur.fetchone()[0]
        load_logo_photos(cur, restaurant_data, restaurant_id)
        load_cuisines(cur, restaurant_data, restaurant_id)
        load_menus(cur, restaurant_data, restaurant_id)
        print(f"Successfully Loaded: {restaurant_data}")


def load_menus(cur, restaurant_data, restaurant_id):
    for menus_data in restaurant_data["menu"]:
        insert_menu(cur, restaurant_id, menus_data)
        menu_id = cur.fetchone()[0]
        create_items(cur, menus_data, menu_id)


def create_items(cur, menus_data, menu_id):
    for items_data in menus_data["items"]:
        insert_items(cur, items_data)
        item_id = cur.fetchone()[0]
        insert_menu_items(cur, menu_id, item_id)


def load_cuisines(cur, restaurant_data, restaurant_id):
    for cusine_data in restaurant_data["cuisines"]:
        insert_cuisines(cur, cusine_data)
        cur.execute("SELECT id FROM cuisines WHERE name = %s;", (cusine_data,))
        cuisine_id = cur.fetchone()[0]
        insert_restaurant_cuisines(cur, restaurant_id, cuisine_id)


def load_logo_photos(cur, restaurant_data, restaurant_id):
    for logo_images_data in restaurant_data["logo_photos"]:
        insert_logo_photos(cur, restaurant_id, logo_images_data)


def export_tables(cur):
    tables_to_export = [
        "restaurants",
        "logo_photos",
        "restaurant_cuisines",
        "cuisines",
        "menus",
        "items",
        "menu_items",
    ]
    for table_name in tables_to_export:
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()

        if rows:
            column_names = [desc[0] for desc in cur.description]

            # Create a CSV file for Created tables
            with open(f"csvs/{table_name}.csv", "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(column_names)
                csv_writer.writerows(rows)

            print(f"Exported data from '{table_name}' to '{table_name}.csv'")


def export_cuisine_search_results(cur):
    cuisines_to_search = [
        "French",
        "Italian",
        "Chinese",
        "Mexican",
        "Thai",
        "American",
        "Mediterranean",
        "Japanese",
        "Spanish",
        "Indian",
        "Vietnamese",
        "Greek",
    ]
    for cuisine in cuisines_to_search:
        cur.execute(f"SELECT * FROM menu_items_by_cuisine_and_price('{cuisine}', 15);")
        rows = cur.fetchall()

        if rows:
            column_names = [desc[0] for desc in cur.description]

            # Create a CSV file for Created tables
            with open(
                f"csvs/query_results/{cuisine}_items_below_15_dollars.csv",
                "w",
                newline="",
            ) as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(column_names)
                csv_writer.writerows(rows)

            print(
                f"Exported data from '{cuisine} Search' to '{cuisine}_items_below_15_dollars.csv'"
            )
