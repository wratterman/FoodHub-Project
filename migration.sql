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
    name VARCHAR
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
    logo_image_id INT REFERENCES logo_photos(id),
    UNIQUE(product_id)
);

-- Create the menu_items table
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    menu_id INT REFERENCES menus(id),
    item_id INT REFERENCES items(id)
);
