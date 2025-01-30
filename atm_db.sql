CREATE DATABASE atm_db;

USE atm_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pin VARCHAR(4) UNIQUE NOT NULL,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

INSERT INTO users (pin, balance) VALUES ('1234', 1000.00);


SELECT * FROM users;

GRANT ALL PRIVILEGES ON atm_db.* TO 'Mayank'@'localhost';

    
