import time
import psycopg2
from psycopg2 import OperationalError
from db import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT


def establish_connection():
    conn = None
    while not conn:
        try:
            conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
            print("Database connection successful")
        except OperationalError as e:
            print(e)
            time.sleep(5)
            print("Retrying connection")
    return conn


def insert_restaurants(cur, restaurant_data):
    cur.execute(
        """
        INSERT INTO restaurants (restaurant_id, name, phone_number, address, type, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (restaurant_id)
        DO UPDATE SET 
            name=EXCLUDED.name 
        RETURNING id;
        """,
        (
            restaurant_data["_id"],
            restaurant_data["name"],
            restaurant_data.get("phone_number", None),
            restaurant_data.get("address", None),
            restaurant_data.get("type", None),
            restaurant_data.get("description", None),
        ),
    )


def insert_cuisines(cur, cusine_data):
    cur.execute(
        """
            INSERT INTO cuisines (name)
            VALUES (%s)
            ON CONFLICT (name)
            DO UPDATE SET 
                name=EXCLUDED.name ;
            """,
        (cusine_data,),
    )


def insert_logo_photos(cur, restaurant_id, logo_images_data):
    cur.execute(
        """
            INSERT INTO logo_photos (restaurant_id, image_url)
            VALUES (%s, %s);
            """,
        (restaurant_id, logo_images_data),
    )


def insert_menu(cur, restaurant_id, menus_data):
    cur.execute(
        """
        INSERT INTO menus (restaurant_id, category_name)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (restaurant_id, menus_data["category_name"]),
    )


def insert_items(cur, items_data):
    cur.execute(
        """
        INSERT INTO items (product_id, name, price, image)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (
            items_data["product_id"],
            items_data["name"],
            items_data["price"],
            items_data["image"],
        ),
    )


def insert_menu_items(cur, menu_id, item_id):
    cur.execute(
        """
        INSERT INTO menu_items (menu_id, item_id)
        VALUES (%s, %s);
        """,
        (menu_id, item_id),
    )


def insert_restaurant_cuisines(cur, restaurant_id, cuisine_id):
    cur.execute(
        """
            INSERT INTO restaurant_cuisines (restaurant_id, cuisine_id)
            VALUES (%s, %s);
            """,
        (restaurant_id, cuisine_id),
    )
