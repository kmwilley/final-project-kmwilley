from flask import Flask, request, jsonify
from sql import DBconnection, execute_read_query, execute_update_query
from creds import Creds
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection
con = DBconnection(Creds.hostname, Creds.username, Creds.password, Creds.database)

# Helper function for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CRUD for Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    sql = "SELECT id, firstname, lastname, email FROM customers"
    customers = execute_read_query(con, sql)
    return jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    hashed_password = hash_password(data['password'])
    sql = f"""INSERT INTO customers (firstname, lastname, email, passwordhash)
                VALUES ('{data['firstname']}', '{data['lastname']}', '{data['email']}', '{hashed_password}')"""
    execute_update_query(con, sql)
    return jsonify({'message': 'Customer added successfully'})

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    hashed_password = hash_password(data['password'])
    sql = f"""UPDATE customers SET firstname='{data['firstname']}', lastname='{data['lastname']}',
                email='{data['email']}', passwordhash='{hashed_password}' WHERE id={id}"""
    execute_update_query(con, sql)
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    sql = f"DELETE FROM customers WHERE id={id}"
    execute_update_query(con, sql)
    return jsonify({'message': 'Customer deleted successfully'})

# CRUD for Books
@app.route('/books', methods=['GET'])
def get_books():
    sql = "SELECT * FROM books"
    books = execute_read_query(con, sql)
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    sql = f"""INSERT INTO books (title, author, genre, status) 
              VALUES ('{data['title']}', '{data['author']}', '{data['genre']}', '{data['status']}')"""
    execute_update_query(con, sql)
    return jsonify({'message': 'Book added successfully'})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    sql = f"UPDATE books SET title='{data['title']}', author='{data['author']}', genre='{data['genre']}', status='{data['status']}' WHERE id={id}"
    execute_update_query(con, sql)
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    sql = f"DELETE FROM books WHERE id={id}"
    execute_update_query(con, sql)
    return jsonify({'message': 'Book deleted successfully'})

# Borrowing Logic