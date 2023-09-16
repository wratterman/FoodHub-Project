import json
import psycopg2
import codecs

from db.db_utils import establish_connection, insert_restaurants, insert_logo_photos, insert_cuisines, insert_menu, insert_items, insert_menu_items, insert_restaurant_cuisines
from db.config import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT

def decode_unicode(text):
    return codecs.decode(text, 'unicode_escape')

# Read the JSON data from the file
with open("FoodHub_data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file, object_hook=lambda d: {k: decode_unicode(v) if isinstance(v, str) else v for k, v in d.items()})

# Connect to the PostgreSQL database
conn = establish_connection()
cur = conn.cursor()

# Insert data into the restaurants table
def load_restaurants(data, cur):
    for restaurant_data in data["restaurants"]:
        print(restaurant_data)
        insert_restaurants(cur, restaurant_data)
        restaurant_id = cur.fetchone()[0]
        load_logo_photos(cur, restaurant_data, restaurant_id)
        load_cuisines(cur, restaurant_data, restaurant_id)
        load_menus(cur, restaurant_data, restaurant_id)

def load_menus(cur, restaurant_data, restaurant_id):
    for menus_data in restaurant_data["menu"]:
        print(menus_data)
        insert_menu(cur, restaurant_id, menus_data)
        menu_id = cur.fetchone()[0]
        create_items(cur, menus_data, menu_id)

def create_items(cur, menus_data, menu_id):
    for items_data in menus_data["items"]:
        insert_items(cur, items_data)
        item_id = cur.fetchone()[0]
        insert_menu_items(cur, menu_id, item_id)
    print(items_data)

def load_cuisines(cur, restaurant_data, restaurant_id):
    for cusine_data in restaurant_data["cuisines"]:
        print(cusine_data)
        insert_cuisines(cur, cusine_data)

        cur.execute("SELECT id FROM cuisines WHERE name = %s;", (cusine_data,))
        cuisine_id = cur.fetchone()[0]

        # Insert into the restaurant_cuisines table
        insert_restaurant_cuisines(cur, restaurant_id, cuisine_id)

def load_logo_photos(cur, restaurant_data, restaurant_id):
    for logo_images_data in restaurant_data["logo_photos"]:
        print(logo_images_data)
        insert_logo_photos(cur, restaurant_id, logo_images_data)


load_restaurants(data, cur)

conn.commit()
conn.close()