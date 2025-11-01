🚀 How to Use
1. Install Dependencies
You must have mysql-connector-python and tabulate installed.

Bash

pip install mysql-connector-python tabulate

2. Configure Database
Before running, open test1.py and edit the mysql.connect() section with your local MySQL password.

Python

# Find this section in test1.py
con = mysql.connect(
    host="localhost",
    user="root",        # Your MySQL username (usually 'root')
    password="prateek@" # <-- CHANGE THIS to your password
)


3. Run
Run the script from your terminal:

Bash

python test1.py
Note: The script will automatically create the bank12 database and the required tables (account and deleted_account) when you run it.
