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
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    book_id, customer_id, borrow_date = data['bookid'], data['customerid'], data['borrowdate']
    
    # Check book availability
    book_check = execute_read_query(con, f"SELECT status FROM books WHERE id={book_id}")
    if not book_check or book_check[0]['status'] != 'available':
        return jsonify({'error': 'Book is not available'}), 400
    
    # Check if customer already has a book borrowed
    customer_check = execute_read_query(con, f"SELECT id FROM borrowingrecords WHERE customerid={customer_id} AND returndate IS NULL")
    if customer_check:
        return jsonify({'error': 'Customer already has a borrowed book'}), 400
    
    # Insert borrowing record
    sql = f"INSERT INTO borrowingrecords (bookid, customerid, borrowdate) VALUES ({book_id}, {customer_id}, '{borrow_date}')"
    execute_update_query(con, sql)
    execute_update_query(con, f"UPDATE books SET status='unavailable' WHERE id={book_id}")
    
    return jsonify({'message': 'Book borrowed successfully'})

@app.route('/return/<int:record_id>', methods=['PUT'])
def return_book(record_id):
    data = request.json
    return_date = data['returndate']
    
    # Get borrowing record
    record = execute_read_query(con, f"SELECT borrowdate, bookid FROM borrowingrecords WHERE id={record_id} AND returndate IS NULL")
    if not record:
        return jsonify({'error': 'Borrowing record not found or book already returned'}), 400
    
    borrow_date = datetime.strptime(record[0]['borrowdate'], '%Y-%m-%d')
    return_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
    late_days = max(0, (return_date_obj - borrow_date - timedelta(days=10)).days)
    late_fee = late_days * 1
    
    # Update borrowing record
    sql = f"UPDATE borrowingrecords SET returndate='{return_date}', late_fee={late_fee} WHERE id={record_id}"
    execute_update_query(con, sql)
    execute_update_query(con, f"UPDATE books SET status='available' WHERE id={record[0]['bookid']}")
    
    return jsonify({'message': 'Book returned successfully', 'late_fee': late_fee})

# View Borrowing Records
@app.route('/borrowings', methods=['GET'])
def get_borrowings():
    sql = "SELECT * FROM borrowingrecords"
    borrowings = execute_read_query(con, sql)
    return jsonify(borrowings)

if __name__ == '__main__':
    app.run(debug=True)
