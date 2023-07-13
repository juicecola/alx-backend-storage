-- --Create table only if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    --Unique identifier for each user
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    
    -- User email (max 255 char)
    email VARCHAR(255) NOT NULL UNIQUE,
    
    --Username (max 255 char)
    name VARCHAR(255)
);
