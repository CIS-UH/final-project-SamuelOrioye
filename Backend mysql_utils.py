import mysql.connector
from mysql.connector import Error

def create_connection(host_Name, user_Name, user_Password, db_Name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_Name,
            user=user_Name,
            passwd=user_Password,
            database=db_Name
        )
        print('Connection successful.')
    except Error as e:
        print(f"The error '{e}' occurred.")  # Log the error for debugging
    return connection


#this is to query and don't want to return anything 
def execute_query(connection, query, values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values) #take query to sql db for execution
        connection.commit() 
        print('query executed successfully.')
    except Error as e:
        print(f"the error '{e}' occurred.")

def execute_read_query(connection, query, values=None):
    cursor = connection.cursor(dictionary=True)
    result = None  # Default to None if no results
    try:
        if values:
            cursor.execute(query, values)  # Use the values if provided
        else:
            cursor.execute(query)  # Otherwise, execute the query without parameters
        result = cursor.fetchall()  # Fetch all results
    except Error as e:
        print(f"The error '{e}' occurred.")
    return result
