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
WHERE c.name ilike 'Mediterranean'
    AND i.price <= 15
ORDER BY restaurant, restaurant_id ASC, price ASC, menu_item;