-- Doc
USE hbnb_dev_db;
SELECT
    u.email, c.name, p.name, p.description, p.number_rooms, p.number_bathrooms, p.max_guest, p.price_by_night, p.latitude, p.longitude
FROM places AS p JOIN users AS u ON p.user_id = u.id JOIN cities AS c ON p.city_id = c.id
ORDER BY p.name DESC;
