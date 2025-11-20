CREATE DATABASE auth;

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert a user with a bcrypt hashed password
-- In Python: bcrypt.hashpw("Admin123".encode(), bcrypt.gensalt())
-- Example hash: $2b$12$... (replace with actual hashed value)
INSERT INTO user(email, password) VALUES (
    'hello@example.com', 
    '$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  -- hashed password
);
