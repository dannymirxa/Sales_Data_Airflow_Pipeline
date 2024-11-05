CREATE TABLE Products (
    product_code VARCHAR(10) NOT NULL,
    product_description VARCHAR(255) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    cost FLOAT NOT NULL,
    price FLOAT NOT NULL
);

INSERT INTO Products (product_code, product_description, product_category, cost, price) VALUES
('P001', 'Product 1', 'Electronics', 40, 80),
('P002', 'Product 2', 'Clothing', 30, 60),
('P003', 'Product 3', 'Groceries', 10, 20),
('P004', 'Product 4', 'Electronics', 50, 100),
('P005', 'Product 5', 'Clothing', 25, 50),
('P006', 'Product 6', 'Groceries', 15, 30),
('P007', 'Product 7', 'Electronics', 60, 120),
('P008', 'Product 8', 'Clothing', 20, 40),
('P009', 'Product 9', 'Groceries', 12, 24),
('P010', 'Product 10', 'Electronics', 70, 140),
('P011', 'Product 11', 'Clothing', 35, 70),
('P012', 'Product 12', 'Groceries', 18, 36),
('P013', 'Product 13', 'Electronics', 45, 90),
('P014', 'Product 14', 'Clothing', 28, 56),
('P015', 'Product 15', 'Groceries', 22, 44),
('P016', 'Product 16', 'Electronics', 65, 130),
('P017', 'Product 17', 'Clothing', 32, 64),
('P018', 'Product 18', 'Groceries', 20, 40),
('P019', 'Product 19', 'Electronics', 55, 110),
('P020', 'Product 20', 'Clothing', 38, 76);
