CREATE TYPE restaurant_type AS ENUM ('dine-in', 'take-out');

-- Create the restaurants table
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    restaurant_id VARCHAR NOT NULL,
    name VARCHAR,
    phone_number VARCHAR,
    address VARCHAR,
    type restaurant_type,
    description VARCHAR,
    UNIQUE(restaurant_id)
);

-- Create the logo_photos table
CREATE TABLE IF NOT EXISTS logo_photos (
    id SERIAL PRIMARY KEY,
    image_url VARCHAR NOT NULL,
    UNIQUE(image_url)
);

-- Create the cuisines table
CREATE TABLE IF NOT EXISTS cuisines (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    UNIQUE(name)
);

-- Create the restaurant_cuisines table
CREATE TABLE IF NOT EXISTS restaurant_cuisines (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    cuisine_id INT REFERENCES cuisines(id),
    UNIQUE(restaurant_id, cuisine_id)
);

-- Create the restaurant_cuisines table
CREATE TABLE IF NOT EXISTS restaurant_logos (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    logo_id INT REFERENCES logo_photos(id),
    UNIQUE(restaurant_id, logo_id)
);

-- Create the menus table
CREATE TABLE IF NOT EXISTS menus (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR,
    UNIQUE(category_name)
);

-- Create the restaurant_cuisines table
CREATE TABLE IF NOT EXISTS restaurant_menus (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    menu_id INT REFERENCES menus(id),
    UNIQUE(restaurant_id, menu_id)
);

-- Create the items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR NOT NULL,
    name VARCHAR,
    price FLOAT,
    image VARCHAR,
    UNIQUE(product_id, name, price, image)
);

-- Create the menu_items table
CREATE TABLE IF NOT EXISTS restaurant_menu_items (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    menu_id INT REFERENCES menus(id),
    item_id INT REFERENCES items(id),
    UNIQUE(restaurant_id, menu_id, item_id)
);

CREATE OR REPLACE FUNCTION menu_items_by_cuisine_and_price(cuisine_type VARCHAR DEFAULT 'Mediterranean', max_price float DEFAULT 15.0)
RETURNS TABLE (
    restaurant_id VARCHAR,
    restaurant VARCHAR,
    product_id VARCHAR,
    menu_item VARCHAR,
    cuisine VARCHAR,
    price float
)
AS $$
DECLARE
    cuisine_type ALIAS FOR $1;
    max_price ALIAS FOR $2;
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        r.restaurant_id AS restaurant_id,
        r.name AS restaurant,
        i.product_id AS product_id,
        i.name AS menu_item,
        c.name AS cuisine,
        i.price AS price
    FROM restaurants r 
    INNER JOIN restaurant_cuisines rc 
        ON r.id = rc.restaurant_id 
    INNER JOIN cuisines c 
        ON rc.cuisine_id = c.id 
    INNER JOIN restaurant_menus rm 
        ON r.id = rm.restaurant_id
    INNER JOIN menus m 
        ON rm.menu_id = m.id
    INNER JOIN restaurant_menu_items rmi 
        ON r.id = rmi.restaurant_id
        AND m.id = rmi.menu_id 
    INNER JOIN items i 
        ON rmi.item_id = i.id 
    WHERE c.name ilike cuisine_type
        AND i.price <= max_price
    ORDER BY restaurant, restaurant_id ASC, price ASC, menu_item;
END;
$$ LANGUAGE plpgsql;