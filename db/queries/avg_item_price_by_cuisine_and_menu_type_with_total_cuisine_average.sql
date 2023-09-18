SELECT
    c.name as cuisine,
    'ALL MENUS' as menu,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine

UNION

SELECT
    c.name as cuisine,
    m.category_name as menu,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN menus m
    ON rmi.menu_id = m.id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine, menu
ORDER BY cuisine, avg_item_price;