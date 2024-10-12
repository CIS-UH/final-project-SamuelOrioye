import mysql.connector

# Function to establish a connection to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host='cis2368fall.cj86u2wm4bbu.us-east-1.rds.amazonaws.com',
        user='admin',  
        password='cis2368Fall4568',  
        database='cis2368falldb'
    )
    return conn

# Function to initialize the database with necessary tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    with open('migrations/create_tables.sql', 'r') as f:
        cursor.execute(f.read(), multi=True)
    conn.commit()
# Commit the transaction to save changes
    cursor.close()
    conn.close()
