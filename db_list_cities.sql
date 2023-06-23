-- Doc
USE hbnb_dev_db;
SELECT c.name, s.name FROM cities AS c JOIN states AS s ON c.state_id = s.id ORDER BY c.name DESC;
