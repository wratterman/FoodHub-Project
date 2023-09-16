SELECT
    r.id AS restaurant_id,
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
    AND r.id = rc.restaurant_id
INNER JOIN menus m 
    ON r.id = m.restaurant_id 
INNER JOIN menu_items mi 
    ON m.id = mi.menu_id 
INNER JOIN items i 
    ON mi.item_id = i.id 
    AND m.id = mi.menu_id
WHERE c.name ilike 'mediterranean' 
    AND i.price <= 15.0
ORDER BY restaurant, restaurant_id, price ASC, menu_item;