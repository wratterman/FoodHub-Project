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
