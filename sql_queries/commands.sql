-- select * from Sales;

-- select * from Products;

SELECT * from Store;

-- SELECT * from Sales sl 
-- INNER JOIN Products p ON
-- sl.product_code = p.product_code
-- INNER JOIN Store st ON
-- sl.store_code = st.store_code;

-- SELECT product_category, 
-- SUM(sales_qty) as sales_qty, 
-- SUM(sales_qty*price) as sales_amount,
-- SUM(sales_qty*cost) as sales_cost,
-- SUM((sales_qty*price) - (sales_qty*cost)) as profit
-- from Sales sl 
-- INNER JOIN Products p ON
-- sl.product_code = p.product_code
-- INNER JOIN Store st ON
-- sl.store_code = st.store_code
-- GROUP BY product_category;