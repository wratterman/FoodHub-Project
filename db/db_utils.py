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
            name=EXCLUDED.name
        RETURNING id;
        """,
        (cusine_data,),
    )


def insert_logo_photos(cur, logo_images_data):
    cur.execute(
        """
        INSERT INTO logo_photos (image_url)
        VALUES (%s)
        ON CONFLICT (image_url)
        DO UPDATE SET 
            image_url=EXCLUDED.image_url
        RETURNING id;
        """,
        (logo_images_data,),
    )


def insert_menu(cur, menus_data):
    cur.execute(
        """
        INSERT INTO menus (category_name)
        VALUES (%s)
        ON CONFLICT (category_name)
        DO UPDATE SET 
            category_name=EXCLUDED.category_name
        RETURNING id;
        """,
        (menus_data["category_name"],),
    )


def insert_items(cur, items_data):
    cur.execute(
        """
        INSERT INTO items (product_id, name, price, image)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id, name, price, image)
        DO UPDATE SET 
            product_id=EXCLUDED.product_id,
            name=EXCLUDED.name,
            price=EXCLUDED.price,
            image=EXCLUDED.image
        RETURNING id;
        """,
        (
            items_data["product_id"],
            items_data["name"],
            items_data["price"],
            items_data["image"],
        ),
    )


def insert_restaurant_menu_items(cur, restaurant_id, menu_id, item_id):
    cur.execute(
        """
        INSERT INTO restaurant_menu_items (restaurant_id, menu_id, item_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (restaurant_id, menu_id, item_id)
        DO UPDATE SET 
            restaurant_id=EXCLUDED.restaurant_id,
            menu_id=EXCLUDED.menu_id,
            item_id=EXCLUDED.item_id;
        """,
        (restaurant_id, menu_id, item_id),
    )


def insert_restaurant_cuisines(cur, restaurant_id, cuisine_id):
    cur.execute(
        """
        INSERT INTO restaurant_cuisines (restaurant_id, cuisine_id)
        VALUES (%s, %s)
        ON CONFLICT (restaurant_id, cuisine_id)
        DO UPDATE SET 
            restaurant_id=EXCLUDED.restaurant_id,
            cuisine_id=EXCLUDED.cuisine_id;
        """,
        (restaurant_id, cuisine_id),
    )


def insert_restaurant_logos(cur, restaurant_id, logo_id):
    cur.execute(
        """
        INSERT INTO restaurant_logos (restaurant_id, logo_id)
        VALUES (%s, %s)
        ON CONFLICT (restaurant_id, logo_id)
        DO UPDATE SET 
            restaurant_id=EXCLUDED.restaurant_id,
            logo_id=EXCLUDED.logo_id;
        """,
        (restaurant_id, logo_id),
    )


def insert_restaurant_menus(cur, restaurant_id, menu_id):
    cur.execute(
        """
        INSERT INTO restaurant_menus (restaurant_id, menu_id)
        VALUES (%s, %s)
        ON CONFLICT (restaurant_id, menu_id)
        DO UPDATE SET 
            restaurant_id=EXCLUDED.restaurant_id,
            menu_id=EXCLUDED.menu_id;
        """,
        (restaurant_id, menu_id),
    )
