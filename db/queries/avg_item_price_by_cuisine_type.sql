SELECT
    c.name as cuisine,
    ROUND(AVG(i.price)::numeric, 2) as avg_item_price
FROM cuisines c
INNER JOIN restaurant_cuisines rc
    ON c.id = rc.cuisine_id
INNER JOIN restaurant_menu_items rmi
    ON rc.restaurant_id = rmi.restaurant_id
INNER JOIN items i
    ON rmi.item_id = i.id
GROUP BY cuisine
ORDER BY avg_item_price;