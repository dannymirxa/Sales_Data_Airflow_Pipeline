CREATE TABLE Store (
    store_code VARCHAR(10) NOT NULL,
    store_name VARCHAR(255) NOT NULL,
    store_region VARCHAR(50) NOT NULL
);

INSERT INTO Store (store_code, store_name, store_region) VALUES
('S001', 'Store 1', 'North'),
('S002', 'Store 2', 'South'),
('S003', 'Store 3', 'East'),
('S004', 'Store 4', 'West'),
('S005', 'Store 5', 'Central'),
('S006', 'Store 6', 'North'),
('S007', 'Store 7', 'South'),
('S008', 'Store 8', 'East'),
('S009', 'Store 9', 'West'),
('S010', 'Store 10', 'Central');
