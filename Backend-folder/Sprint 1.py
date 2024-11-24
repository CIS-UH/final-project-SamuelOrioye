import flask
from flask import jsonify
from flask import request
import creds
from mysql_utils import create_connection
from mysql_utils import execute_read_query
from mysql_utils import execute_query

app = flask.Flask(__name__)  # Set up application
app.config['DEBUG'] = True

# Connection to MySQL database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)


@app.route('/api/investors', methods=['GET'])
def get_all_investors():
    # Check if the database connection is None (not established)
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500
    
    sql = 'SELECT * FROM investor'  # SQL query to fetch all investors
    try:
        # Execute the query
        investors = execute_read_query(conn, sql)
        
        # If no investors are found, return a 404 message
        if not investors:
            return jsonify({"message": "No investors found"}), 404
        
        # Return the list of investors as a JSON response
        return jsonify(investors)
    
    except Exception as e:
        # If an error occurs, return a 500 error with the exception message
        return jsonify({"message": f"An error occurred: {e}"}), 500


@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    print("DEBUG: /api/stocks route called")  # Debug log
    if conn is None:
        print("DEBUG: Database connection failed")  # Debug log
        return jsonify({"message": "Database connection failed"}), 500

    sql = 'SELECT * FROM stock'
    try:
        print("DEBUG: Executing SQL query: SELECT * FROM stock")  # Debug log
        stocks = execute_read_query(conn, sql)
        print(f"DEBUG: Query result: {stocks}")  # Debug log

        if not stocks:
            print("DEBUG: No stocks found")  # Debug log
            return jsonify({"message": "No stocks found"}), 404

        return jsonify(stocks)
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")  # Debug log
        return jsonify({"message": f"An error occurred: {e}"}), 500



# GET method to fetch a specific stock by ID
@app.route('/api/stocks/<id>', methods=['GET'])
def get_stock(id):
    sql = "SELECT * FROM stock WHERE id = %s"
    selected_stock = execute_read_query(conn, sql, (id,))  # Pass id as a tuple
    return jsonify(selected_stock)


# POST method for creating a new stock
@app.route("/api/stocks", methods=['POST'])
def add_stock():
    try:
        stock_data = request.get_json()
        stockname = stock_data['stockname']
        abbreviation = stock_data['abbreviation']
        currentprice = stock_data['currentprice']

        sql = "INSERT INTO stock (stockname, abbreviation, currentprice) VALUES (%s, %s, %s)"
        values = (stockname, abbreviation, currentprice)
        execute_query(conn, sql, values)

        return jsonify({"message": "Stock added successfully."})
    except Exception as e:
        return jsonify({'Error': f'Error occurred: {e}'})


# PUT method for updating a stock
@app.route('/api/stocks/<id>', methods=['PUT'])
def update_stock(id):
    try:
        stock_data = request.get_json()
        stockname = stock_data['stockname']
        abbreviation = stock_data['abbreviation']
        currentprice = stock_data['currentprice']

        # Prepare the SQL statement to update the stock details
        sql = "UPDATE stock SET stockname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
        values = (stockname, abbreviation, currentprice, id)

        # Execute the query
        execute_query(conn, sql, values)

        return jsonify({"message": f'Stock with ID {id} successfully updated.'})
    except Exception as e:
        return jsonify({'Error': f'Error occurred: {e}'})


# DELETE method for deleting a stock
@app.route('/api/stocks/<id>', methods=['DELETE'])
def delete_stock(id):
    try:
        sql = 'DELETE FROM stock WHERE id = %s'
        execute_query(conn, sql, (id,))
        return jsonify({'Message': f'Stock {id} deleted successfully.'})
    except Exception as e:
        return jsonify({"Error": f'Error occurred: {e}'})


@app.route('/api/stocktransactions', methods=['POST'])
def add_stock_transaction():
    try:
        transaction_data = request.get_json()
        investorid = transaction_data['investorid']
        stockid = transaction_data['stockid']
        quantity = transaction_data['quantity']

        # Check current possession of stock
        possession_sql = """
        SELECT SUM(quantity) AS current_possession FROM stocktransaction 
        WHERE investorid = %s AND stockid = %s
        """
        possession = execute_read_query(conn, possession_sql, (investorid, stockid))[0]['current_possession'] or 0

        if possession + quantity < 0:
            return jsonify({"Error": "Sale quantity exceeds current possession."}), 400

        # Insert transaction
        sql = "INSERT INTO stocktransaction (investorid, stockid, quantity) VALUES (%s, %s, %s)"
        values = (investorid, stockid, quantity)
        execute_query(conn, sql, values)

        return jsonify({"message": "Transaction added successfully."})
    except Exception as e:
        return jsonify({'Error': f'Error occurred: {e}'})


# GET method to fetch all bonds
@app.route('/api/bonds', methods=['GET'])
def get_all_bonds():
    sql = 'SELECT * FROM bond'
    bonds = execute_read_query(conn, sql)
    return jsonify(bonds)


# GET method for fetching a specific bond by ID
@app.route('/api/bonds/<id>', methods=['GET'])
def get_bond(id):
    sql = "SELECT * FROM bond WHERE id = %s"
    selected_bond = execute_read_query(conn, sql, (id,))
    return jsonify(selected_bond)


# POST method for creating a new bond
@app.route("/api/bonds", methods=['POST'])
def add_bond():
    try:
        bond_data = request.get_json()
        bondname = bond_data['bondname']
        abbreviation = bond_data['abbreviation']
        currentprice = bond_data['currentprice']

        sql = "INSERT INTO bond (bondname, abbreviation, currentprice) VALUES (%s, %s, %s)"
        values = (bondname, abbreviation, currentprice)
        execute_query(conn, sql, values)

        return jsonify({"message": "Bond added successfully."})
    except Exception as e:
        return jsonify({'Error': f'Error occurred: {e}'})


# PUT method for updating a bond
@app.route('/api/bonds/<id>', methods=['PUT'])
def update_bond(id):
    try:
        bond_data = request.get_json()
        bondname = bond_data['bondname']
        abbreviation = bond_data['abbreviation']
        currentprice = bond_data['currentprice']

        sql = "UPDATE bond SET bondname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
        values = (bondname, abbreviation, currentprice, id)
        execute_query(conn, sql, values)

        return jsonify({"message": f'Bond with ID {id} successfully updated.'})
    except Exception as e:
        return jsonify({'Error': f'Error occurred: {e}'})


# DELETE method for deleting a bond
@app.route('/api/bonds/<id>', methods=['DELETE'])
def delete_bond(id):
    try:
        sql = 'DELETE FROM bond WHERE id = %s'
        execute_query(conn, sql, (id,))
        return jsonify({'Message': f'Bond {id} deleted successfully.'})
    except Exception as e:
        return jsonify({"Error": f'Error occurred: {e}'})


# Main app runner
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
