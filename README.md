
# Database Systems Project
# Name: Riley Phan

## Database design and query
### Phase 1: Schema
My database contains datasets for a café:
- **products**: the products (beverages + pastries) sold, columns:
	- productID (int, primary key)
	- productName: name of products on menu
	- productType: beverage or pastry
	- price
	- calories
	- ingredients 
- **employees**: employees at the café, columns:
	- employeeID (int, primary key)
	- firstName
	- lastName
	- shift_preference: day or night
	- employment_type: full or part time
	- hourly_rate
	- date_of_birth
	- email
	- phone_number
- **customers**: customers who are in the loyalty program, columns):
	- customerID (int, primary key)
	- firstName
	- lastName
	- phoneNo
	- loyalty_points: accrued loyalty points
	- favorite_product (int, foreign key references products)
	- birthday
- **orders**: orders from loyalty customers in 2 weeks, columns:
	- orderID (int, primary key)
	- customerID (int, foreign key references customers): customer orders using loyalty id
	- employeeID (int, foreign key references employees): employee in charge at register
	- productID: ordered product
	- total_amount
	- loyalty: loyalty points earned
	- date_order
- **schedule**: work hours of employees, columns:
	- scheduleID (int, primary key)
	- date
	- employeeID (int, foreign key references employees): employee assigned
	- role: barista, manager, register, baker
	- shift: day or night
	- total_hours
	- start_time
	- end_time
	- overtime_hours	
- **inventory**: a list of inventories for tracking, columns:
	- inventoryName (varchar, primary key)
	- remaining_quantity: in stock count
	- reorderThreshold: threshold quantity to restock inventory
- **suppliers**: contact of inventory suppliers, columns:
	- id (int, primary key)
	- name: name of supplier
	- contact: supplier phone number
	- product_provided (varchar, foreign key references inventory): matching product in inventory
- **feedback**: feedbacks from customers, columns:
	- feedbackID (int, primary key)
	- customerID (int, foreign key references customers): loyalty customer who left a feedback
	- customer_name
	- email
	- date
	- score: score 1 to 5
	- comments: additional comments
	- overall_experience: based on score, Good or Bad

I use [mockaroo](https://www.mockaroo.com/) to generate these datasets by specifying the desired fields, column types and any constraints. 

### Phase 2: Query
Run the dump.sql to import my schema into target MySQL server
To run the .sql file containing the queries, open the SQL script in Workbench and use CTRL/CMD+ENTER to run the selected query by putting your cursor right after its ending semi-colon.
- If query works, a query result table will appear
- If query doesn't work, an error will pop up on the log monitor

### Phase 3: Python
To run the .py script, run *pip install pymysql*. Run the script either via an IDE or in a terminal (python front-end.py). The script will ask you to:
- **Enter your password:** type in password for MySQL server --> Lets you connect to my db in the server
- Each query will be run subsequently, with a task description each time a query function runs
- **Level 1 - Query 1 - get_employee(db):** will ask to input "day"/"night" and "full time"/"part time" to query employees from the employees table
- **Level 1 - Query 4 - top_orders(db):** will ask to input number between 1 and 20 to find the top most ordered product(s)
- **Level 2 - Query 1 - add_employee_record(db):** will ask to input employee data to be added to the employees table
- **Level 2 - Query 2 - delete_employee_schedule(db):** will ask to input a number between 1 and 80 to delete the employee's schedule who has the matching id 
- **Level 2 - Query 4 - delete_customer(db):** will ask to input a number between 1 and 250 to delete a customer record from the customers table (won't work anyway due to foreign key constraints)

## Challenges
- It took me quite a while to look around for inspirations  and come up with a valid (business) idea for my database
- Designing the ER diagram and database schema so that the tables and relationships make sense
- Ensuring the data makes sense when generating it with AI 
- (I forgot my MySQL server password) 
- Importing the data into Workbench, not too challenging but can be tricky to get used to
- Creating proper foreign key constraints for the tables. This is definitely one of the most complicated part that requires a lot of planning in advance to avoid overcomplicating it further (ex: having conflicting constraints and not recognizing it) 
	- Also, the process in Workbench asks that I do certain things in order, which can be confusing and time-consuming
- All of the try except blocks when accepting user inputs
- The lack of documentation on mysql-connector