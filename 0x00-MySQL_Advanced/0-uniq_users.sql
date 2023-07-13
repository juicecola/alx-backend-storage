--Create table only if it doesn't exist
CREATE TABLE IF NOT EXIT users (
	--Unique identifier for each user
	id INTEGER PRIMARY KEY AUTO_INCREMENT,

	--User email (max 255 char)
	email VARCHAR(255) NOT NULL UNIQUE,

	--User name (max 255 char)
	name VARCHAR(255)
);
