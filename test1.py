import mysql.connector as mysql
from tabulate import tabulate  
try:
    # Establish connection
    con = mysql.connect(
        host="localhost",
        user="root",
        password="prateek@" 
    )
    cur = con.cursor()

    # Create and use the database
    cur.execute("CREATE DATABASE IF NOT EXISTS bank12")
    cur.execute("USE bank12")

    # --- Table 1: account ---
   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS account (
        customer_acno BIGINT(12) PRIMARY KEY,
        first_name VARCHAR(36) NOT NULL,
        last_name VARCHAR(36) NOT NULL,
        father_name VARCHAR(35),
        mother_name VARCHAR(35),
        age INT(3),
        gender VARCHAR(10) NOT NULL,
        account_type VARCHAR(35),
        opening_date DATE NOT NULL,
        opening_time TIME NOT NULL,
        balance BIGINT(20),
        mobile BIGINT(10) UNIQUE,
        address VARCHAR(35),
        IFSC_code VARCHAR(20), 
        occupation VARCHAR(35),
        status VARCHAR(10) DEFAULT 'open'
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deleted_account (
        customer_acno BIGINT(12) PRIMARY KEY,
        first_name VARCHAR(36) NOT NULL,
        last_name VARCHAR(36) NOT NULL,
        father_name VARCHAR(35),
        mother_name VARCHAR(35),
        age INT(3),
        gender VARCHAR(10) NOT NULL,
        account_type VARCHAR(35),
        opening_date DATE NOT NULL,
        opening_time TIME NOT NULL,
        balance BIGINT(20),
        mobile BIGINT(10) UNIQUE,
        address VARCHAR(35),
        IFSC_code VARCHAR(20),
        occupation VARCHAR(35),
        status VARCHAR(10) DEFAULT 'close'
    )
    """)

    # Header list for tabulate (Fixes the broken header string)
    HEADERS = [
        "Acc. No", "First Name", "Last Name", "Father", "Mother", "Age",
        "Gender", "Acc. Type", "Open Date", "Open Time", "Balance",
        "Mobile", "Address", "IFSC", "Occupation", "Status"
    ]

    print("-" * 75)
    print(" " * 22, "Class 12th Project")
    print("-" * 75)
    print(" " * 18, "Bank Management")
    print("-" * 75)
    print(" " * 13, "Welcome to Prateek Bank")
    print("-" * 75)
    print(" " * 8, "Management Records of customer account")

    def add():
        print(" " * 10, "Now Insert customer account details", " " * 10)
        try:
            i = int(input("Enter customer_acno: "))
            n1 = input("Enter customer first_Name: ")
            n2 = input("Enter customer last_Name : ")
            fn = input("Enter Father Name: ")
            mn = input("Enter Mother Name: ")
            a = int(input("Enter customer Age: "))
            g = input("Enter Gender: ")
            p = input("Enter customer account type: ")
            d = input("Enter opening date (YYYY-MM-DD): ")
            t = input("Enter opening Time (HH:MM:SS): ")
            b = int(input("Enter balance: "))
            m = int(input("Enter customer Mobile Number: "))
            ad = input("Enter customer address: ")
            c = input("Enter IFSC code: ")  # Changed to string input
            o = input("Enter customer occupation: ")
            s = input("Enter customer status (e.g., open): ")

            
            q = ("INSERT INTO account VALUES "
                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            
            values = (i, n1, n2, fn, mn, a, g, p, d, t, b, m, ad, c, o, s)
            
            cur.execute(q, values)
            con.commit()
            print("\nNew data inserted successfully!")
        except mysql.Error as err:
            print(f"Error: {err}")
            con.rollback()
        except ValueError:
            print("Invalid input. Please enter numbers for numeric fields.")

    def displayall():
        print(" " * 10, "Record List of customer", " " * 10)
        q = "SELECT * FROM account"
        cur.execute(q)
        data = cur.fetchall()
        if not data:  
            print("Record list is empty")
        else:
            
            print(tabulate(data, headers=HEADERS, tablefmt="grid"))

    def search():
        try:
            i = int(input("Enter customer_acno to be searched: "))
            q = "SELECT * FROM account WHERE customer_acno = %s"
            cur.execute(q, (i,))
            data = cur.fetchall()
            if not data:
                print("No record available")
            else:
               
                print(tabulate(data, headers=HEADERS, tablefmt="grid"))
        except ValueError:
            print("Invalid input. Please enter a number.")

    def update():
        try:
            id = int(input("Enter customer acno to be updated: "))
            q = "SELECT * FROM account WHERE customer_acno = %s"
            cur.execute(q, (id,))
            data = cur.fetchone()  
            
            if not data:
                print("No record found!!!!")
            else:
                
                b = int(input("Enter New amount: "))
                update_q = "UPDATE account SET balance = %s WHERE customer_acno = %s"
                cur.execute(update_q, (b, id))
                con.commit()
                print("Record is updated successfully")
        except ValueError:
            print("Invalid input. Please enter numbers.")
        except mysql.Error as err:
            print(f"Error: {err}")
            con.rollback()

    def delete():
        try:
            id = int(input("Enter customer acno to be deleted: "))
            q = "SELECT * FROM account WHERE customer_acno = %s"
            cur.execute(q, (id,))
            data = cur.fetchone()
            
            if not data:
                print("No record found!!!!")
            else:
               
                insert_q = ("INSERT INTO deleted_account VALUES "
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cur.execute(insert_q, data)
                
                delete_q = "DELETE FROM account WHERE customer_acno = %s"
                cur.execute(delete_q, (id,))
                
                con.commit()
                print("Record moved to recycle bin successfully")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except mysql.Error as err:
            print(f"Error: {err}")
            con.rollback()

    def display_recyclebin():
        print(" " * 10, "Recycle Bin", " " * 10)
        q = "SELECT * FROM deleted_account"
        cur.execute(q)
        data = cur.fetchall()
        if not data:
            print("Recycle bin is empty")
        else:
           
            print(tabulate(data, headers=HEADERS, tablefmt="grid"))

    def delete_recyclebin():
        try:
            id = int(input("Enter customer acno to be deleted: "))
            q = "SELECT * FROM deleted_account WHERE customer_acno = %s"
            cur.execute(q, (id,))
            data = cur.fetchone()
            
            if not data:
                print("No record found!!!!")
            else:
               
                delete_q = "DELETE FROM deleted_account WHERE customer_acno = %s"
                cur.execute(delete_q, (id,))
                con.commit()
                print("Record is deleted from recycle bin successfully!!!!!")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except mysql.Error as err:
            print(f"Error: {err}")
            con.rollback()

    def restore_record():
        try:
            id = int(input("Enter customer acno to be restored: "))
           
            q = "SELECT * FROM deleted_account WHERE customer_acno = %s"
            cur.execute(q, (id,))
            data = cur.fetchone()
            
            if not data:
                print("No record found!!!!")
            else:
           
                insert_q = ("INSERT INTO account VALUES "
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cur.execute(insert_q, data)
                
                delete_q = "DELETE FROM deleted_account WHERE customer_acno = %s"
                cur.execute(delete_q, (id,))
                
                con.commit()
                print("Record restored successfully")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except mysql.Error as err:
            print(f"Error: {err} (Account number might already exist in main table)")
            con.rollback()

    # --- Main Loop ---
    while True:
        print("-" * 75)
        print("1 - Add new customer account")
        print("2 - Display all records")
        print("3 - Search record")
        print("4 - Update a record")
        print("5 - Delete a record (Move to Recycle Bin)")
        print("6 - Open recycle bin")
        print("7 - Delete from recycle bin (Permanent)")
        print("8 - Restore deleted record from recycle bin")
        print("9 - Exit")
        print("-" * 75)
        
        try:
            ch = int(input("Enter your choice: "))
            
            if ch == 1:
                add()
            elif ch == 2:
                displayall()
            elif ch == 3:
                search()
            elif ch == 4:
                update()
            elif ch == 5:
                delete()
            elif ch == 6:
                display_recyclebin()
            elif ch == 7:
                delete_recyclebin()
            elif ch == 8:
                restore_record()
            elif ch == 9:
                print("\nThank you for using Prateek Bank!")
                break
            else:
                print("Invalid choice!!!! Please choose from 1-9.")
        
        except ValueError:
            print("Invalid choice! Please enter a number.")

except mysql.Error as err:
    print(f"Failed to connect to MySQL: {err}")
finally:
   
    if 'con' in locals() and con.is_connected():
        cur.close()
        con.close()
        print("MySQL connection is closed.")