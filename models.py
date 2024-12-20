# SQL Queries for all operations

CREATE_INVESTOR = "INSERT INTO investor (firstname, lastname) VALUES (%s, %s)"
GET_ALL_INVESTORS = "SELECT * FROM investor"
GET_INVESTOR_BY_ID = "SELECT * FROM investor WHERE id=%s"
UPDATE_INVESTOR = "UPDATE investor SET firstname=%s, lastname=%s WHERE id=%s"
DELETE_INVESTOR = "DELETE FROM investor WHERE id=%s"

CREATE_STOCK = "INSERT INTO stock (stockname, abbreviation, currentprice) VALUES (%s, %s, %s)"
GET_ALL_STOCKS = "SELECT * FROM stock"
UPDATE_STOCK = "UPDATE stock SET stockname=%s, abbreviation=%s, currentprice=%s WHERE id=%s"
DELETE_STOCK = "DELETE FROM stock WHERE id=%s"

CREATE_BOND = "INSERT INTO bond (bondname, abbreviation, currentprice) VALUES (%s, %s, %s)"
GET_ALL_BONDS = "SELECT * FROM bond"
UPDATE_BOND = "UPDATE bond SET bondname=%s, abbreviation=%s, currentprice=%s WHERE id=%s"
DELETE_BOND = "DELETE FROM bond WHERE id=%s"

CREATE_STOCK_TRANSACTION = "INSERT INTO stocktransaction (investorid, stockid, quantity) VALUES (%s, %s, %s)"
CREATE_BOND_TRANSACTION = "INSERT INTO bondtransaction (investorid, bondid, quantity) VALUES (%s, %s, %s)"
GET_STOCK_TRANSACTIONS = "SELECT * FROM stocktransaction WHERE investorid=%s"
GET_BOND_TRANSACTIONS = "SELECT * FROM bondtransaction WHERE investorid=%s"
DELETE_STOCK_TRANSACTION = "DELETE FROM stocktransaction WHERE id=%s"
DELETE_BOND_TRANSACTION = "DELETE FROM bondtransaction WHERE id=%s"

