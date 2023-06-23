-- Doc
USE hbnb_dev_db;
SELECT 
    r.text, u.email, p.name
FROM reviews AS r JOIN users AS u ON r.user_id = u.id JOIN places AS p ON r.place_id = p.id
ORDER BY r.text DESC;
