DROP TABLE restaurants CASCADE;
DROP TABLE logo_photos CASCADE;
DROP TABLE cuisines CASCADE;
DROP TABLE restaurant_cuisines CASCADE;
DROP TABLE menus CASCADE;
DROP TABLE items CASCADE;
DROP TABLE menu_items CASCADE;
DROP FUNCTION menu_items_by_cuisine_and_price(VARCHAR, float) CASCADE;