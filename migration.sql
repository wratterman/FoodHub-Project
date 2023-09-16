-- Create the restaurants table
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    restaurant_id VARCHAR NOT NULL,
    name VARCHAR,
    phone_number VARCHAR,
    address VARCHAR,
    type VARCHAR,
    description VARCHAR,
    UNIQUE(restaurant_id)
);

-- Create the logo_photos table
CREATE TABLE logo_photos (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    image_url VARCHAR NOT NULL
);

-- Create the cuisines table
CREATE TABLE cuisines (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    UNIQUE(name)
);

-- Create the restaurant_cuisines table
CREATE TABLE restaurant_cuisines (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    cuisine_id INT REFERENCES cuisines(id)
);

-- Create the menus table
CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(id),
    category_name VARCHAR
);

-- Create the items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR NOT NULL,
    name VARCHAR,
    price FLOAT,
    image VARCHAR
);

-- Create the menu_items table
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    menu_id INT REFERENCES menus(id),
    item_id INT REFERENCES items(id)
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
    INNER JOIN menus m 
        ON r.id = m.restaurant_id 
    INNER JOIN menu_items mi 
        ON m.id = mi.menu_id 
    INNER JOIN items i 
        ON mi.item_id = i.id 
    WHERE c.name ilike cuisine_type
        AND i.price <= max_price
    ORDER BY restaurant, restaurant_id ASC, price ASC, menu_item;
END;
$$ LANGUAGE plpgsql;