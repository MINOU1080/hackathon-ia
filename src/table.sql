CREATE DATABASE ing IF NOT EXISTS;

-- Table des clients
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate DATE,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    address VARCHAR(255),
    segment_code VARCHAR(10)
);

-- Table des produits actifs
CREATE TABLE products_active (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_type VARCHAR(100) NOT NULL,
    product_name VARCHAR(100),
    opened_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table des produits clôturés
CREATE TABLE products_closed (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_type VARCHAR(100) NOT NULL,
    product_name VARCHAR(100),
    opened_date DATE,
    closed_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'closed',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ✅ Table unique des transactions
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10),
    description VARCHAR(255),
    transaction_type VARCHAR(50)
);
