import mysql.connector
from mysql.connector import Error
import hashlib
import os
from creds import Creds

def DBconnection():
    # Establish a database connection using credentials
    con = None
    try:
        con = mysql.connector.connect(
            host = Creds.hostname,
            user = Creds.username,
            password = Creds.password,
            database = Creds.database
        )
        print("Connection successful")
    except Error as e:
        print("Connection unsuccessful due to Error:", e)
    return con

# Execute query function for SELECT operations
def execute_read_query(con, sql, params=None):
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(sql.params)
        return cursor.fetchall()
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()

# Execute query function for INSERT/UPDATE/DELETE operations
def execute_update_query(con, sql, params=None):
    cursor = con.cursor()
    try:
        cursor.execute(sql, params)
        con.commit()
        return cursor.lastrowid
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()

# Password hashing using hashlib with salt
def hash_password(password):
    salt = os.urandom(32) # Generate a random 32-byte salt
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password # Store salt + hash together

def verify_password(password, stored_hash):
    salt = stored_hash[:32] # Extract salt from stored hash
    stored_password = stored_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_hash == stored_password

# CRUD OPERATIONS FOR CUSTOMERS
def get_all_customers(con):
    return execute_read_query(con, "SELECT id, firstname, lastname, email FROM customers")

def get_customers_by_id(con, customer_id):
    return execute_read_query(con, "SELECT id, firstname, lastname, email FROM customers WHERE id = %s", (customer_id,))

def add_customer(con, firstname, lastname, email, password):
    hashed_password = hash_password(password)
    return execute_update_query(con, """"
        INSERT INTO customers (firstname, lastname, email, passwordhash)
        VALUES (%s, %s, %s, %s)
    """, (firstname, lastname, email, hashed_password))

def update_customer(con, customer_id, firstname=None, lastname=None, email=None, password=None):
    fields = []
    params = []

    if firstname:
        fields.append("firstname = %s")
        params.append(firstname)
    if lastname:
        fields.append("lastname = %s")
        params.append(lastname)
    if email:
        fields.append("email = %s")
        params.append(email)
    if password:
        fields.append("passwordhash = %s")
        params.append(hash_password(password))

    params.append(customer_id)

    return execute_update_query(con, f"UPDATE customers SET {', '.join(fields)} WHERE id = %s", tuple(params))

def delete_customer(con, customer_id):
    return execute_update_query(con, "DELETE FROM customers WHERE id = %s", (customer_id,))

        
        