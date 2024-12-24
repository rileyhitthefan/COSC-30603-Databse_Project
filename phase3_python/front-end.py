import pymysql
import time

def connect(password): 
    """ Connect to db on server using input password """
    db = None
    try:
        print("Connecting to database...")
        db = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root@1234@@',
            database = 'cafe_db_riley'
        )
        print("Connected")
    
    except pymysql.Error as e:
        print(e)
    
    return db

# LEVEL 1
def get_employee(db):
    """ Find all employees based on specified shift preference and employment type """
    cursor = db.cursor()
    
    # Define shift
    try:
        shift_pref  = input("Enter day or night: ")
        employment = input("Enter employment type (full or part time): ")
        if shift_pref in ["day", "night"] and employment in ["full time", "part time"]:
            # Query: 
            query = (
                'SELECT * '
                'FROM employees '
                'WHERE shift_preference = %s '
                'AND employment_type = %s '
            )
            
            data = (shift_pref, employment,)
            cursor.execute(query, data)
            result = cursor.fetchall()
            
            time.sleep(1)
            if result:
                for row in result:
                    print(row)
        else:
            print("No employees found.")
            
    except Exception as e:
        print("Error: ", e)
        
    cursor.close()

def restock_contact(db):
    """ find the inventory that need restocking (remaining quantity less than stock threshold) and the suppliers of those inventory"""
    cursor = db.cursor()
    
    try:
        # Query: 
        query = (
            'SELECT i.inventoryName, "supplies needed", s.name, s.contact '
            'FROM suppliers s '
            'INNER JOIN inventory i '
            'ON s.product_provided = i.inventoryName '
            'WHERE i.reorderThreshold < i.remaining_quantity '
        )
        
        time.sleep(1)
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for row in result:
                print(row)
        else:
            print("No inventory needs restocking.")
    
    except Exception as e:
        print("Error: ", e)
        
    cursor.close()
    
def most_hours(db):
    """ find id and name of employees who have worked the most hours for each role """
    cursor = db.cursor()
    
    try:
    # Query: 
        query = (
            'SELECT s1.employeeID, CONCAT(e.firstName, " ", e.lastName) AS eName, s1.role, s1.total_hours '
            'FROM schedule s1 '
            'INNER JOIN employees e '
            'ON s1.employeeID = e.employeeID '
            'WHERE s1.total_hours = ( '
            'SELECT MAX(s2.total_hours) '
            'FROM schedule s2 '
            'WHERE s1.role = s2.role '
            ') '
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        time.sleep(1)
        if result:
            for row in result:
                print(row)
        else:
            print("No hours found.")

    except Exception as e:
        print("Error: ", e)
        
    cursor.close()       
            
def top_orders(db):
    """ find the product name of the top K most ordered products as well as the number of timesa
    they were ordered in descending order """
    cursor = db.cursor()
    
    try: 
        k = input("Enter number of top products (1-20): ")
        k = int(k)
        if 1 <= k <= 20:
            # Query: 
            query = (
                'SELECT p.productName, COUNT(o.productID) AS order_count '
                'FROM orders o '
                'LEFT JOIN products p '
                'ON o.productID = p.productID '
                'GROUP BY p.productName '
                'ORDER BY order_count DESC '
                'LIMIT %s '
            )
            
            data = (k,)
            cursor.execute(query, data)
            result = cursor.fetchall()
            
            time.sleep(1)
            if result:
                for row in result:
                    print(row)
                    
        else:
            print("No orders found.")
    except ValueError:
        print("Please enter an integer from 1 to 20")
    except Exception as e:
        print("Error: ", e)
    
    cursor.close()
    
# LEVEL 2
def add_employee_record(db):
    """Add a new employee record to the employees table"""
    cursor = db.cursor()
    
    try:
        firstName = input("Enter first name: ")
        lastName = input("Enter last name: ")
        shift_preference = input("Enter shift preference (day/night): ")
        employment_type = input("Enter employment type (full time/part time): ")
        hourly_rate = input("Enter hourly rate: ")
        hourly_rate = float(hourly_rate)
        date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
        email = input("Enter email: ")
        phone_number = input("Enter phone number: ")
        
        query = (
            'INSERT INTO employees (firstName, lastName, shift_preference, employment_type, hourly_rate, date_of_birth, email, phone_number) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
        )
        
        data = (firstName, lastName, shift_preference, employment_type, hourly_rate, date_of_birth, email, phone_number,)
        cursor.execute(query, data)
        db.commit()
        
        time.sleep(1)
        print("Employee record added.")
    
    except ValueError:
        print("Please enter valid values.")
        
    except Exception as e:
        print("Error: ", e)
        db.rollback()
    
    cursor.close()
    
def delete_employee_schedule(db):
    """Delete an employee record from the schedule table"""
    cursor = db.cursor()
    
    try: 
        # Query:
        query = (
            'DELETE FROM schedule '
            'WHERE employeeID = %s '
        )
        
        employeeID = input("Enter employee ID (1-80): ")
        employeeID = int(employeeID)  
        
        data = (employeeID,)
        cursor.execute(query, data)
        db.commit()
        
        time.sleep(1)
        print("Schedule deleted.")
        
    except ValueError:
        print("Please enter an integer from 1 to 80")
        
    except Exception as e:
        print("Error: ", e)
        db.rollback()
    
    cursor.close()
    
def update_inventory(db):
    """Update the inventory table by adjusting the reorder threshold to 200 for Chocolate"""
    cursor = db.cursor()
    
    try: 
        # Query:
        query = (
            'UPDATE inventory '
            'SET reorderThreshold = 200 '
            'WHERE inventoryName = "Chocolate" '
        )
        print("Updating reorder threshold for Chocolate to 200...")
        cursor.execute(query)
        db.commit()
        
        time.sleep(1)
        print("Inventory updated.")
    
    except Exception as e:
        print("Error: ", e)
        db.rollback()
    
    cursor.close()
    
def delete_customer(db):
    """Delete a customer record from the customers table"""
    cursor = db.cursor()
    
    try: 
        customerID = input("Enter customer ID (1-250): ")
        customerID = int(customerID)
        
        # Query:
        query = (
            'DELETE FROM customers '
            'WHERE customerID = %s '
        )
        
        data = (customerID,)
        cursor.execute(query, data)
        
        db.commit()
    
    except ValueError:
        print("Please enter an integer from 1 to 250")
        
    except pymysql.Error as e:
        time.sleep(1)
        print("Error: ", e)
        print("Do not delete customer records.")
        
    cursor.close()

if __name__ == "__main__":
    password = input("Enter password: ")
    db = connect(password)
    time.sleep(1)
    
    # Run queries
    print("1. Find all employees based on shift preference and employment type")
    get_employee(db)
    time.sleep(2)
    
    print("2. Find contact of inventory that needs restocking")
    restock_contact(db)
    time.sleep(2)
    
    print("3. Find employees who have worked the most hours by role")
    most_hours(db)
    time.sleep(2)
    
    print("4. Find top K most ordered products")
    top_orders(db)
    time.sleep(2)
    
    print("5. Add a new employee record")
    add_employee_record(db)
    time.sleep(2)
    
    print("6. Delete an employee record from the schedule table")
    delete_employee_schedule(db)
    time.sleep(2)
    
    print("7. Update the inventory table reorder threshold")
    update_inventory(db)
    time.sleep(2)
    
    print("8. Delete a customer record")
    delete_customer(db)

    print("All queries done. Closing connection...")
    db.close()