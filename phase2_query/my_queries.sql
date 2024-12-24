-- LEVEL 1
-- 1. One query must be a basic SELECT/FROM/WHERE query: select all part-time employees who are wanting to work night shift
-- (simple query, it works)
SELECT * FROM employees
WHERE shift_preference = "night" AND employment_type = "part time";

-- 2. One query must answer a question that needs to join 2 or more tables: find the inventory that need restocking
-- (remaining quantity less than stock threshold) and the suppliers of those inventory (works) 
SELECT i.inventoryName, "supplies needed", s.name, s.contact FROM suppliers s
INNER JOIN inventory i
ON s.product_provided = i.inventoryName
WHERE i.reorderThreshold < i.remaining_quantity;

-- 3. One query must have a subquery: find id and name of employees who have worked the most hours by role
-- (cashier, baker, barista, shift manager)
SELECT s1.employeeID, CONCAT(e.firstName, " ", e.lastName) AS eName, s1.role, s1.total_hours 
FROM schedule s1
INNER JOIN employees e
ON s1.employeeID = e.employeeID
WHERE s1.total_hours = (
	SELECT MAX(s2.total_hours)
    FROM schedule s2
    WHERE s1.role = s2.role
);

-- 4. One query must have an aggregate function and GROUP BY clause: find the product name of the top 10 most ordered products
-- as well as the number of times they were ordered in descending order (works)
SELECT p.productName, COUNT(o.productID) AS order_count
FROM orders o
LEFT JOIN products p
ON o.productID = p.productID
GROUP BY p.productName
ORDER BY order_count DESC
LIMIT 10;

-- LEVEL 2
-- 1. One query must add a record to one or more tables: Add new employee record to the employees table
INSERT INTO employees (firstName, lastName, shift_preference, employment_type, hourly_rate, date_of_birth, email, phone_number)
VALUES ("Steve", "Rogers", "night", "full time", 20, "1918-07-04", "srogers@avengers.com", "012-345-789");
	-- Query the newly added row
	SELECT * FROM employees WHERE phone_number = "012-345-789";

-- 2. One query must delete a record from one or more tables.
	-- Query before modifying
    SELECT * FROM schedule WHERE employeeID = 22;
    -- Delete employee record
    DELETE FROM schedule
    WHERE employeeID = 22;
    -- Requery the record from schedule table
    SELECT * FROM schedule WHERE employeeID = 22;

-- 3. You have foreign key ON UPDATE constraints that make sense on a table/tables 
-- and write an SQL query to demonstrate how one of them works
	-- I have constraint ON UPDATE NO ACTION for foreign key product_provided in suppliers tables, since I want to update my
    -- inventory record without losing the contacts info of my supplier
    -- Updating reorderThreshold for "chocolate" from 100 to 200 will work (no error) but doesn't result in any difference 
    -- in the suppliers table
    -- (Updating, for example, record of "chocolate" to "chocolate chips" won't work since
    -- that will violates referential integrity)
	UPDATE inventory 
	SET reorderThreshold = 200
    WHERE inventoryName = "Chocolate";
    -- Select suppliers for chocolate
    SELECT * FROM suppliers WHERE product_provided = "Chocolate";
    
-- 4. You have foreign key ON DELETE constraints that make sense on a table/tables 
-- and write an SQL query to demonstrate how one of them works.
	-- I have constraint ON DELETE RESTRICT for the foreign key customerID in feedback table, since I want to retain info
    -- of all customers with a loyalty customerID, as well as their feedbacks
    -- Delete customer records that match the first 2 row in feedback table, which returns an error (doesn't work)
    DELETE FROM customers
    WHERE customerID = (
		SELECT customerID FROM feedback
        LIMIT 1
    );