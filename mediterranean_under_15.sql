SELECT 
    r.name AS restaurant,
    I.name AS menu_item,
    c.name AS cuisine,
    I.price AS price
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
WHERE c.name ilike 'mediterranean' 
    AND i.price <= 15.0
ORDER BY restaurant, price ASC, item;